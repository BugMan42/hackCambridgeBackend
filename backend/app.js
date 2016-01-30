var express = require('express');
var mongoose = require('mongoose');
var fs = require('fs');
var http = require('http');
var bodyParser = require('body-parser');

var app = express();
require('./models/index').initialize();

mongoose.connect('mongodb://localhost/backend');

app.use(bodyParser.json());

http.createServer(app).listen(8080, function(){
    console.log('Listening on port 8080');
});