const express = require('express');

const router = express.Router();


router.get('/', (req, res) => {
    let loginGoneWrong = '';

    try {
        console.log('abriu main')
        // res.status(200).sendFile('pages/login.html', {root:'src/views'})
        res.status(200).render('pages/main', {loginGoneWrong: loginGoneWrong})

    } catch (error) {
        console.log('erro get login')
        console.log(error)
    }
    
})

module.exports = router;
