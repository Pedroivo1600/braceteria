from flask import Flask, request, jsonify
from pyModbusTCP.server import ModbusServer
from time import sleep
from random import uniform
from threading import Thread
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Importar o CORS


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")  # Permitir apenas o cliente da porta 3000

socketio.emit("testando", 30)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


#Create an instance of ModbusServer
SERVER_ADDRESS = '10.103.16.11'
SERVER_PORT = 502
server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block = True)


def connect_to_modbusServer(data):

    print(data)

    tamanho = [int(data["tamanho"])]
    cobertura = [int(data["cobertura"])]
    topping = [int(data["topping"])]
    start_process = [True]
    
    try:
 
        print('Starting server...')
        
        server.start()
        print('teste')
        # print(help(server.data_bank.get_coils))
        #robo_ocupado = server.data_bank.get_coils(0)
        robo_ocupado = True

        #server.data_bank.get_holding_registers
        
        print('Server is online')
        
        while robo_ocupado:
            server.data_bank.set_input_registers(0, tamanho)
            server.data_bank.set_input_registers(1, cobertura)
            server.data_bank.set_input_registers(2, topping)
            server.data_bank.set_input_registers(3, start_process)

            sleep(.5)
      
    except:
    
        print('Shutting down server...')
        
        start_process = False
        server.stop()
        
        print('Server is offline')

@app.route('/get_variable', methods=['GET'])
def get_variable():
    print('estou aquiiii')
    # Retorna o valor da variável global
    return jsonify({"variable_value": False})


@app.route('/receive_data', methods=['POST'])
def receive_data():
    global robot_busy
    print(robot_busy, 'hellooooo')


    if robot_busy:
        return jsonify({"status": "error", "message": "Robô ocupado, tente novamente mais tarde."}), 409



    data = request.get_json()
    tamanho = data.get('tamanho')
    cobertura = data.get('cobertura')
    topping = data.get('topping')

    if tamanho == "pequeno":
        tamanho = 1
    elif tamanho == "medio":
        tamanho = 2
    elif tamanho == "grande":
        tamanho = 3


    if cobertura == "chocolate":
        cobertura = 1
    elif cobertura == "caramelo":
        cobertura = 2
    elif cobertura == "frutas":
        cobertura = 3
    elif cobertura == "sem_cobertura":
        cobertura = 0

    if topping == "granola":
        topping = 1
    elif topping == "confete":
        topping = 2
    elif topping == "nozes":
        topping = 3
    elif topping == "sem_topping":
        topping = 0

    


    data_to_robot = {
        "tamanho": tamanho,
        "cobertura": cobertura,
        "topping": topping
    }

    ##Botao do form EJS ganha propriedade disabled

    # Aqui você pode processar os dados, como enviar para o robô
    print(f"Tamanho: {tamanho}, Cobertura: {cobertura}, Topping: {topping}")


    try:

        # Thread(target=connect_to_modbusServer, args=(data_to_robot,)).start()
        connect_to_modbusServer(data_to_robot)
        print('shit')
    except Exception as e:
        print('ola')
        print(e)

    # Retorna uma resposta JSON
    return jsonify({"status": "success", "message": "Pedido recebido!"})


if __name__ == '__main__':
    print("Iniciando o servidor...")
    app.run(port=5000)
    # socketio.run(app, port=5000, debug=True, use_reloader=False)


