const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')

const mainRouter = require('./src/routes/main')


const app = express();

app.use(express.static(path.join(__dirname, 'public')))
app.set('views', path.join(__dirname, 'src/views'))
app.set('view engine', 'ejs')   


app.use(bodyParser.urlencoded({ extended: false })); //middleware para entender requisição via form (post)

app.use('/', mainRouter);


app.listen(3000, () => {
    console.log('Servidor foi iniciado')
})