var express = require('express');
var router = express.Router();
var word = require('mongoose').model('WordEN');
var http = require('http');
var querystring = require('querystring');

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

router.get('/', function(req, res, next){
    word.find({}, function(err, data) {
        if(!err) {
            var randWord = data[Math.floor(Math.random() * data.length)].word;
            console.log(randWord);
            var NUMBER_OF_WORDS = 50;
            var dataQuery = querystring.stringify({
                word: randWord,
                nRecom: NUMBER_OF_WORDS
            });
            var options = {
                host: '172.20.1.43',
                path: '/',
                port: '5000',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Length': Buffer.byteLength(dataQuery)
                }
            };
            var post_req = http.request(options, function(response, error) {
                if (error) console.log(error);
                response.setEncoding('utf8');
                response.on('data', function (chunk) {
                    console.log(chunk);
                    res.status(200).end(chunk);
                });

            });
            post_req.write(dataQuery);
            post_req.end();

        }
        else {
            res.status(404).end("Not Found");
        }
    });
});

router.get('/all', function(req, res, next) {
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