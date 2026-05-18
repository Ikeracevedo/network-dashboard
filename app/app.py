from flask import Flask, jsonify, render_template, request
import subprocess
import socket
import platform
import datetime

# Inicializador de Flask
app = Flask(__name__)

# Endpoint de la ruta principal del dashboard
@app.route('/')
def index():
    return render_template('index.html')


# Endpoint para verificar si el host responde ping
@app.route('/api/check')
def verificador_host():
    host = request.args.get('host','')

    if not host:
        return jsonify({'error':'Debes enviar un host valido'}), 400

    # El comando entre linux y windows puede variar por eso se usa el metodo para comprobar el SO 
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    try:
        output = subprocess.run(command, capture_output=True, timeout=5)
        alive = output.returncode == 0
    except Exception as e:
        alive = False

    return jsonify({
        'host': host,
        'alive': alive,
        'timestamp':datetime.datetime.now().isoformat()
    })


# Endpoint para verifiacr si un puerto esta abierto en un host

@app.route('/api/port')
def verificador_puerto():
    host = request.args.get('host','')
    port = request.args.get('port','')

    if not host or not port:
        return jsonify({'error': 'Debes enviar un host y un port'}), 400
    
    try:
        port = int(port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        open_port = result == 0
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'host':host,
        'port': port,
        'open': open_port,
        'timestamp': datetime.datetime.now().isoformat()
    })


# Endponint estado general del servidor
@app.route('/api/status')
def status():
    return jsonify({
        'service':'network-dashoard',
        'status':'running',
        'timestamp': datetime.datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)