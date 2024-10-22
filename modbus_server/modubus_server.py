from pyModbusTCP.server import ModbusServer
from time import sleep
from random import uniform

#Create an instance of ModbusServer
SERVER_ADDRESS = '10.103.16.130'
SERVER_PORT = 502
server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block = True)

try:
 print('Starting server...')
 server.start()
 print('Server is online')
 while True:
  print('oi')
    # n_lados = [int(input("Entre com o número de lados:"))]
    # comprimento = [int(input("Entre com o comprimento dos lados do polígono:"))]
    # server.data_bank.set_input_registers(0, n_lados)
    # server.data_bank.set_input_registers(1, comprimento)
except:
 print('Shutting down server...')
 server.stop()
 print('Server is offline')



from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/collect_data', methods=['POST'])
def collect_data():
    sabor = request.form.get('sabor')
    cobertura = request.form.get('cobertura')
    topping = request.form.get('topping')

    # Aqui você pode fazer algo com os dados recebidos, como imprimir ou armazenar em um banco de dados
    print(f"Sabor: {sabor}, Cobertura: {cobertura}, Topping: {topping}")

    return "Pedido recebido!"

if __name__ == '__main__':
    app.run(debug=True)