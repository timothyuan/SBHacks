var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var path = require('path');
var cors = require('cors');
var multer = require('multer');
var spawn = require("child_process").spawn;
var request = require('request');
var user = require('./routes/user.js');

var storage = multer.diskStorage({
	destination: function (req, file, callback) {
		callback(null, './');
	},
	filename: function (req, file, callback) {
		callback(null, 'upload.dat');
	}
});

var upload = multer({storage: storage}).single('file');

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use('/user', user);
app.use(express.static(__dirname + '/dist/socialclient/'));

app.get('/image/:image', function(req, res) {
  res.sendFile(path.join(__dirname, '/uploads/'+req.params.image));
});

app.post('/check', function(req, res){
  upload(req, res, function(err) {
    var pythonProcess = spawn('python',["facerec_f.py", "-i" , "upload.dat"]);
    pythonProcess.stdout.on('data', (data) => {
        message = data.toString();
        console.log(message);
        var isAllowed = true;
        if(message=='No match\n'){
          isAllowed = false;
        }
        request({
          url: 'http://b206bebb.ngrok.io/switch',
          qs: { q:isAllowed}}, function(err, response, body){
                res.status(200).send({isAllowed: isAllowed});
        });
    });
  })
});

app.get('*', function(req, res) {
  res.sendFile(__dirname + '/dist/socialclient/index.html')
})

app.listen(3000, '0.0.0.0', function() {
    console.log('Listening to port: ' + 3000);
});
