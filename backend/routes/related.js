var express = require('express');
var router = express.Router();
var word = require('mongoose').model('WordEN');
var http = require('http');

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

router.get('/', function(req, res, next){
    word.find({}, function(err, data) {
        if(!err) {
            var options = {
                host: 'http://172.20.1.43',
                path: '/',
                port: '5000',
                method: 'POST'
            };
            var NUMBER_OF_WORDS = 50;
            var req = http.request(options, function(response) {
                res.status(200).end(response);
            });
            var randWord = data[Math.floor(Math.random() * data.length)];
            req.write("fname={}&lname={}".format(randWord, NUMBER_OF_WORDS));
            req.end();
        }
        else {
            res.status(404).end("Not Found");
        }
    });
});



module.exports = router;