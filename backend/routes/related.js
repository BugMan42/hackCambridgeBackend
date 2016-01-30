var express = require('express');
var router = express.Router();

// get all related words
router.get('/', function(req, res, next){
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
    /*word.find({}, function(err, data) {
        if(!err) {
            res.status(200).json(data);
        }
    })*/
});



module.exports = router;