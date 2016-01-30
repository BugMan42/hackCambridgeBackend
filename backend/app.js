var express = require('express');
var mongoose = require('mongoose');
var fs = require('fs');
var http = require('http');
var bodyParser = require('body-parser');

var app = express();
require('./models/index').initialize();

mongoose.connect('mongodb://localhost/backend');

app.use(bodyParser.json());

//app.use(expressWinston.logger(config.winston_options));

var wordRouter = require('./routes/words');

app.use('/words' ,wordRouter);

var userRouter = require('./routes/users');

app.use('/users' ,userRouter);

var authenticationRouter = require('./routes/authentication');

app.use('/authentication', authenticationRouter);

http.createServer(app).listen(8080, function(){
    console.log('Listening on port 8080');
});