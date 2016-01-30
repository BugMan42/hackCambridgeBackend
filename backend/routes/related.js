var express = require('express');
var router = express.Router();
var word = require('mongoose').model('WordEN');

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

router.get('/', function(req, res, next){
    word.find({}, function(err, data) {
        if(!err) {
            var randWord = data[Math.floor(Math.random() * data.length)];
            var xmlHttp = new XMLHttpRequest();
            var NUMBER_OF_WORDS = 50;
            xmlHttp.open("POST", "http://172.20.1.43:5000", false);
            xmlHttp.send("fname={}&lname={}".format(randWord, NUMBER_OF_WORDS));
            var response =  xmlHttp.responseText;
            res.status(200).end(response);
        }
        else {
            res.status(404).end("Not Found");
        }
    });
});



module.exports = router;