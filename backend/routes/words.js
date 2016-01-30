var express = require('express');
var router = express.Router();
var word = require('mongoose').model('WordEN');
var ObjectId = require('mongoose').Types.ObjectId;



// get all words
router.get('/', function(req, res, next){
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
router.get('/:id', function(req, res, next){
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

router.post('/', function(req, res, next) {
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


router.delete('/:id', function(req, res, next) {
    var wordId = req.params.id;
    word.remove({_id: new ObjectId(wordId)}, function(err){
        if(!err) {
            res.status(200).end("Deleted");
        }
        else {
            console.log(err);
        }
    });

});

router.patch('/:id', function(req, res, next) {
    var userId = req.params.id;
    var userData = req.body;
    word.update({_id: userId}, {$set: userData}, function(err) {
        if(!err) {
            res.status(200).end("Updated");
        }
        else {
            console.log(err);
        }
    });

});

module.exports = router; //When calling require('words'), we get the router.