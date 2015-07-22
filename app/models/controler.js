var mongoose = require('mongoose');

module.exports = mongoose.model('controler',{
	name : {type: String, default: ''},
        id : {type: Number, default:0}
});
