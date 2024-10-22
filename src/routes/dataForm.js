const express = require('express');
const axios = require('axios');  // Certifique-se de importar o axios

const router = express.Router();


router.post('/collect_data', async (req, res) => {
    const { sabor, cobertura, topping } = req.body;

    try {
        // Envia os dados para o servidor Flask
        const response = await axios.post('http://127.0.0.1:5000/receive_data', {
            sabor,
            cobertura,
            topping
        });

        // Trate a resposta do servidor Flask conforme necessário
        console.log(response.data);
        res.send('Pedido enviado para o robô!');
    } catch (error) {
        console.error(error);
        res.status(500).send('Erro ao enviar pedido para o robô.');
    }
});

module.exports = router;
