var express = require('express');
var router = express.Router();

// get all related
router.get('/', function(req, res, next){
    /*word.find({}, function(err, data) {
        if(!err) {
            res.status(200).json(data);
        }
    })*/
});



module.exports = router; //When calling require('words'), we get the router.