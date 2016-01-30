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
            req.write("word={}&nRecom={}".format(randWord, NUMBER_OF_WORDS));
            req.end();
        }
        else {
            res.status(404).end("Not Found");
        }
    });
});

outer.get('/all', function(req, res, next) {
    var data = [
        {
            "_id": "56aceeee90e57deb4cc3b92a",
            "word": "patat22a",
            "definition": "yeaaaahhhhh",
            "user": "56acd8d9e2ede8b73bd04ed5",
            "__v": 0
        },
        {
            "_id": "56acf6eb670d463254be353d",
            "word": "potato",
            "definition": "yeaaaahhhhh",
            "user": "56acebd3dd27683a4cfed751",
            "__v": 0
        },
        {
            "_id": "56ad1c01979b0f3c12592560",
            "word": "game",
            "definition": "yeaaaahhhhh",
            "user": "56acebd3dd27683a4cfed751",
            "__v": 0
        },
        {
            "_id": "56ad1c08979b0f3c12592561",
            "word": "football",
            "definition": "yeaaaahhhhh",
            "user": "56acebd3dd27683a4cfed751",
            "__v": 0
        },
        {
            "_id": "56ad1c0d979b0f3c12592562",
            "word": "baseball",
            "definition": "yeaaaahhhhh",
            "user": "56acebd3dd27683a4cfed751",
            "__v": 0
        },
        {
            "_id": "56ad1c12979b0f3c12592563",
            "word": "incredible",
            "definition": "yeaaaahhhhh",
            "user": "56acebd3dd27683a4cfed751",
            "__v": 0
        }
    ];
    res.status(200).json(data);
});



module.exports = router;