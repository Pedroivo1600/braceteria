from flask import Flask, request, jsonify
from pyModbusTCP.server import ModbusServer
from time import sleep
from threading import Thread
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
#CORS(app, origins=['http://10.102.1.148:30200'])
CORS(app)  # Permite acesso de qualquer origem (cuidado em produção)



# Define o servidor Modbus
SERVER_ADDRESS = '10.103.16.11'
SERVER_PORT = 502
server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block=True)

# Função para iniciar o servidor Modbus
def start_modbus_server():
    start_process = [False]
    print('oi')
    try:
        server.start()
        print('Modbus Server iniciado')
        server.data_bank.set_input_registers(3, start_process)
        while True:
            sleep(1)  # Mantém o servidor ativo
    except Exception as e:
        print(f'Erro no servidor Modbus: {e}')
        server.stop()

# Função para processar o pedido do usuário
def process_request(data):

    stop_robot = [1]
    # Extrai as variáveis e define os registros Modbus
    porcoes_flocos = [int(data["porcoes_flocos"])]
    porcoes_baunilh = [int(data["porcoes_baunilha"])]
    #cobertura = [int(data["cobertura"])]
    
    
    try:
        while stop_robot == [1]:
            server.data_bank.set_input_registers(0, porcoes_flocos)
            server.data_bank.set_input_registers(1, porcoes_baunilh)
            #server.data_bank.set_input_registers(2, cobertura)
            stop_robot = server.data_bank.get_holding_registers(4)
            sleep(.1)
            start_process = [True]
            server.data_bank.set_input_registers(3, start_process)
            print(stop_robot)

            sleep(.5)
        

        start_process = [False]
        server.data_bank.set_input_registers(3, start_process)

        # Simula o processamento do pedido no robô
        print(data)
        #sleep(15)  # Tempo de processamento do robô
        print("Processamento concluído")
    except KeyError as e:
        print(e)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # global robot_busy
    # if robot_busy:
    #     return jsonify({"status": "error", "message": "Robô ocupado, tente novamente mais tarde."}), 409

    data = request.get_json()
    porcoes_flocos = data.get('porcoes_flocos')
    porcoes_baunilha = data.get('porcoes_baunilha')
    #cobertura = data.get('cobertura')

    # Converte o pedido para os valores esperados
    data_to_robot = {
        "porcoes_flocos": 0 if porcoes_flocos == "zero" else 1 if porcoes_flocos == "um" else 2 if porcoes_flocos == "dois" else 3,
        "porcoes_baunilha": 0 if porcoes_baunilha == "zero" else 1 if porcoes_baunilha == "um" else 2 if porcoes_baunilha == "dois" else 3
        #"cobertura": 1 if cobertura == "chocolate" else 2 if cobertura == "caramelo" else 3 if cobertura == "frutas" else 0
    }
    
    # Processa o pedido em uma nova thread para não bloquear o Flask
    process_request(data_to_robot)
    return jsonify({"status": "success", "message": "Pedido recebido!"})

@app.route('/start_order', methods=['GET'])
def start_order():
    pega_copo_move = [True]
    server.data_bank.set_input_registers(5, pega_copo_move)
    inicial_process = [True]
    while inicial_process == [True]:
        print('entrei aqui')
        inicial_process = server.data_bank.get_holding_registers(6)
        print(inicial_process)

        sleep(.5)
    
    pega_copo_move = [False]
    server.data_bank.set_input_registers(5, pega_copo_move)
    return jsonify({'start_process': True})


@app.route('/get_variable', methods=['GET'])
def get_variable():
    print('estou aquiiii')
    # Retorna o valor da variável global
    return jsonify({"variable_value": False})

if __name__ == '__main__':
    # Inicia o servidor Modbus em uma thread separada
    Thread(target=start_modbus_server).start()
    # Inicia o servidor Flask
    #app.run(port=5000)
    app.run(host='0.0.0.0', port=5000)
    #app.run(host="10.102.1.207", port=30201)


