var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var path = require('path');
var cors = require('cors');
var user = require('./routes/user.js');
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use('/user', user);


app.get('/image/:image', function(req, res) {
  res.sendFile(path.join(__dirname, '/uploads/'+req.params.image));
});


app.listen(3000);
