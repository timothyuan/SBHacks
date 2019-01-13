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
app.use(express.static(__dirname + '/dist/socialclient/'));


app.get('/image/:image', function(req, res) {
  res.sendFile(path.join(__dirname, '/uploads/'+req.params.image));
});

app.get('*', function(req, res) {
  res.sendFile(__dirname + '/dist/socialclient/index.html')
})

app.listen(3000, '0.0.0.0', function() {
    console.log('Listening to port: ' + 3000);
});
