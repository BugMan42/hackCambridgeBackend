var express = require('express');
var wordsRouter = express.Router();
var word = require('mongoose').model('WordEN');
var ObjectId = require('mongoose').Types.ObjectId;
var querystring = require('querystring');
var http = require('http');
var https = require('https');

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

// get all words
wordsRouter.get('/', function(req, res, next){
    word.find({}, function(err, data) {
        if(!err) {
            res.status(200).json(data);
        }
        else {
            res.status(404).end("Not Found");
        }
    })
});

// get all words of a user
wordsRouter.get('/:id', function(req, res, next){
    var wordId = req.params.id;
    word.find({user:new ObjectId(wordId)}, function(err, data) {
        if(!err) {
            res.status(200).json(data);
        }
        else {
            res.status(404).end("Not Found");
        }
    })
});

wordsRouter.post('/translation', function(req, res, next) {
    var destLang = 'en-' + req.body.destLang;
    var dataQuery = querystring.stringify({
        key: 'trnsl.1.1.20160130T213138Z.61f3d3183a7aea66.576cd55ad6fca5eebf5c5cb9a97c8249f897f142',
        text: req.body.word,
        lang: destLang
    });
    var options = {
        host: 'translate.yandex.net',
        path:  '/api/v1.5/tr.json/translate?' + dataQuery,
        rejectUnauthorized: false
    };
    var get_req = https.get(options, function(response, error) {
        if (error) {
            console.log(error);
            res.status(400).end("ERROR");
        }
        else {
            response.setEncoding('utf8');
            response.on('data', function (chunk) {
                var aux = JSON.parse(chunk).text;
                res.status(200).end(JSON.stringify(aux[0]));
            });
        }

    });
    get_req.on('error', function(e) {
        console.log('ERROR: ' + e.message);
    });
});

wordsRouter.post('/', function(req, res, next) {
    var wordData = req.body;
    var newWord = new word(wordData);
    newWord.save(function(err, saved) {
        if(!err) {
            res.status(200).json(saved);
        } else {
            console.log(err);
        }
    })
});

wordsRouter.post('/discardedWords', function(req, res, next) {
    var discardedWords = req.body;
    console.log("DISCARDED " + discardedWords);
    var dataQuery = JSON.stringify(discardedWords);
    var options = {
        host: '172.20.1.43',
        path: '/discardedWords',
        port: '5000',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(dataQuery)
        }
    };
    var post_req = http.request(options, function(response, error) {
        if (error) {
            console.log(error);
            res.status(400).end("NOPE");
        }
        else {
            response.setEncoding('utf8');
            response.on('data', function (chunk) {
                console.log(chunk);
                res.status(200).end("discardedWords Done");
            });
        }

    });
    post_req.write(dataQuery);
    post_req.end();
});

wordsRouter.post('/acceptedWords', function(req, res, next) {
    var acceptedWords = req.body;
    console.log("ACCEPTED " + acceptedWords);
    var dataQuery = JSON.stringify(acceptedWords);
    var options = {
        host: '172.20.1.43',
        path: '/acceptedWords',
        port: '5000',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(dataQuery)
        }
    };
    var post_req = http.request(options, function(response, error) {
        if (error) console.log(error);
        response.setEncoding('utf8');
        response.on('data', function (chunk) {
            console.log(chunk);
            res.status(200).end("AcceptedWords Done");
        });

    });
    post_req.write(dataQuery);
    post_req.end();
});

wordsRouter.delete('/:id', function(req, res, next) {

    word.remove({_id: new ObjectId(req.params.id)}, function(err){
        if(!err) {
            res.status(200).end("Word deleted");
        }
    });

});

wordsRouter.patch('/:id', function(req, res, next) {
    var userId = req.params.id;
    var userData = req.body;
    word.update({_id: userId}, {$set: userData}, function(err) {
        if(!err) {
            res.status(200).end("Word updated");
        }
        else {
            console.log(err);
        }
    });

});

module.exports = wordsRouter; //When calling require('words'), we get the router.