var express = require('express');
var mongoose = require('mongoose');
var fs = require('fs');
var http = require('http');
var config = require('./config');
var bodyParser = require('body-parser');

var app = express();
require('./models/index').initialize();

mongoose.connect(config.db_path);

app.use(bodyParser.json());

//app.use(expressWinston.logger(config.winston_options));

var wordRouter = require('./routes/words');

app.use('/words' ,wordRouter);

http.createServer(app).listen(8080, function(){
    console.log('Listening on port 8080');
});