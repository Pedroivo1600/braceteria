
async function teste(event){
    event.preventDefault();  // Impede o envio do formulário automaticamente
    try {
        // Faz a requisição para o backend
        const response = await fetch('http://10.102.1.202:5000/get_variable');
        if (!response.ok) {
          throw new Error('Erro na requisição');
        }
  
        // Converte a resposta em JSON
        const data = await response.json();
        console.log(data)
  
        const robotBusy = data.variable_value; // Verifica o valor retornado

        if (robotBusy === false) {
            event.target.submit(); // Faz o submit para a rota especificada no `action` do formulário
            document.getElementById('submit-btn').innerHTML = "Fazendo"
            document.getElementById('submit-btn').disabled = true
            console.log('xxxx')

            // const responseForm = await fetch('http://127.0.0.1:3000/collect_data');
            // console.log(responseForm)

        } else {
            alert("Condição não atendida. O formulário não foi enviado.");
        }

      } catch (error) {
        console.error('Erro:', error);
      }
}

async function mostrarFormulario(event) {
  document.getElementById('start-div').style.display = 'none';
  document.getElementById('wait-div').style.display = 'block';

  try {
    const response = await fetch('http://10.102.1.202:5000/start_order', { status: true });
    if (!response.ok) {
      throw new Error('Erro na requisição');
    }

    const data = await response.json()
    console.log(data)
  
    document.getElementById('wait-div').style.display = 'none';
    document.getElementById('form-div').style.display = 'block';
  } catch (error) {
    console.error('Erro ao iniciar o pedido:', error);
  }


}




