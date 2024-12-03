const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')

const mainRouter = require('./src/routes/main')
const dataRouter = require('./src/routes/dataForm')


const app = express();

app.use(express.static(path.join(__dirname, 'public')))
app.set('views', path.join(__dirname, 'src/views'))
app.set('view engine', 'ejs')   


app.use(bodyParser.urlencoded({ extended: false })); //middleware para entender requisição via form (post)

app.use('/', mainRouter);
app.use('/', dataRouter)


// app.listen(3000, () => {
//     console.log('Servidor foi iniciado')
// })

const HOST = '10.102.1.202'; // IP no qual o servidor vai rodar
const PORT = 30200;         // Porta que o servidor vai usar

app.listen(PORT, HOST, () => {
    console.log(`Servidor foi iniciado em http://${HOST}:${PORT}`);
});