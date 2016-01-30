var mongoose = require('mongoose');
var Schema = mongoose.Schema;

module.exports = function() {
    var wordsENSchema = new Schema({
        word: {type: String, required: true},
        definition: {type: String, required: false},
        audio: {data: Buffer, contentType: String}
    });

    mongoose.model('WordEN', wordsENSchema, 'words');
};