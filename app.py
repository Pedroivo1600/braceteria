from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    sabor = data.get('sabor')
    cobertura = data.get('cobertura')
    topping = data.get('topping')

    # Aqui você pode processar os dados, como enviar para o robô
    print(f"Sabor: {sabor}, Cobertura: {cobertura}, Topping: {topping}")

    # Retorna uma resposta JSON
    return jsonify({"status": "success", "message": "Pedido recebido!"})

if __name__ == '__main__':
    print("Iniciando o servidor...")
    app.run(port=5000, debug=True)