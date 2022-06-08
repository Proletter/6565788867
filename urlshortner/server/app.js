const express = require('express')
const app = express()
const morgan = require('morgan')
app.use(express.json())
app.use(morgan('tiny'))


app.use(express.urlencoded({ extended: true }));

app.use('/', require('./routes/redirect'));
app.use('/api', require('./routes/shortner'));

console.log(app.get("env"))

const port = process.env.PORT || 1337
app.listen(port,()=>{
    console.log(`listening on port ${port}`)
})