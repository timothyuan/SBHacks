var express = require('express');
var mysql = require('mysql');
var multer = require('multer');
var router = express.Router();
var path = require('path');
var bodyParser = require('body-parser');
var config = require('./config.js');

var con = mysql.createConnection(config);

con.connect(function(err) {
	if (err) throw err;
	console.log("connected!");
});

var storage = multer.diskStorage({
	destination: function (req, file, callback) {
		callback(null, './uploads');
	},
	filename: function (req, file, callback) {
		req.date = Date.now();
		callback(null, req.body.username+ '_' + req.date+path.extname(file.originalname));
	}
});

/*Multer accepts a single file with the name photo. This file will be stored in request.file*/

var upload = multer({storage: storage}).single('file');

router.post('/register', function(req, res){
	var user = req.body.username;
	var pass = req.body.password;
	var sql = "INSERT INTO users (username, password) VALUES ('"+user+"', '"+pass+"')";
	con.query(sql, function (err, result) {
		if (err) {
			console.log(err);
			res.status(400);
			res.end()
		}else{
			console.log('inserted');
			res.status(200).send({username: user});
		}
	});
});

router.post('/login', function(req, res){
	var user = req.body.username;
	var pass = req.body.password;
	var sql = "SELECT * FROM users WHERE username = '"+user+"' AND password = '"+pass+"'";
	con.query(sql, function (err, result) {
		if (err) throw err;
		if(result[0]==null){
			console.log('DNE');
			res.status(404);
			res.end();
		}else{
			console.log('exists');
   			//res.status(200);
   			//res.end();
   			res.status(200).send({id : result[0].id});
   		}
   	});
});

router.post('/upload', function(req, res) {
	upload(req, res, function(err) {
		if(err) {
			console.log(err);
			res.status(400);
			res.end();
		}else{
			var sql = "INSERT INTO images (user_id, image_name, date) VALUES ("+req.body.id+", '"+req.file.filename+"',"+req.date+")";
			con.query(sql, function (err, result) {
				if (err) {
					console.log(err);
					res.status(400);
				}else{
					console.log('image inserted');
					res.status(200);
				}
			});
			res.send({id: req.body.id});
		}
	})
});

router.post('/images', function(req, res){
	var id = req.body.id;
	var sql = "SELECT image_name FROM images WHERE user_id = "+id;
	con.query(sql, function (err, result) {
		if (err) throw err;
		console.log(result);
		if(result[0]==null){
			console.log('no images');
			res.status(404);
			res.end();
		}else{
			console.log('images found');
   			var images = [];
   			for(var i=0; i < result.length; i++){
   				images.push(result[i].image_name)
   			}
   			res.status(200).send({images : images});
   		}
   	});
});

module.exports = router;
