var mongoose = require('mongoose');
var obj = Schema.Types.ObjectId;
var Schema = mongoose.Schema;

module.exports = function() {
    var wordsENSchema = new Schema({
        user: {type: obj, required: true},
        word: {type: String, required: true, unique: true},
        definition: {type: String, required: false},
        audio: {data: Buffer, contentType: String}
    });

    wordsENSchema.index({user: 1, word:1}, {unique: true});

    mongoose.model('WordEN', wordsENSchema, 'words');
};