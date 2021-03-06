const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const schema = new Schema({
    guildID: {
        type: String,
        required: true,
        unique: true
    },
    prefix: {
        type: String,
        required: false,
        default: "?"
    },
    comandos: [{
        type: String,
        required: false
    }],
    chatsDisable: [{
        type: String,
        required: false
    }],
    chatsDisableMsg:{ //aviso == false || deletar == true
        type: Boolean,
        required: false,
        default: false
    },
    numMute: {
        type: Number,
        required: false,
        default: 0
    },
    numKick: {
        type: Number,
        required: false,
        default: 0
    },
    numSoftBan: {
        type: Number,
        required: false,
        default: 0
    },
    numBan: {
        type: Number,
        required: false,
        default: 0
    },
    tempoMute: { //segundos || 0 == 'perma
        type: Number,
        required: false,
        default: 3600
    },
    tempoAviso: { //segundos
        type: Number,
        required: false,
        default: 3600
    },
    tempoBan: { //segundos || o == 'perma'
        type: Number,
        required: false,
        default: 3600
    },
    localMsgAviso: { //"dm" == true || "chat" == false
        type: Boolean,
        required: false,
        default: false
    },
    banWords: { //ativado == true || desativado == false
        type: Boolean,
        required: false,
        default: false
    },
    banWordsList: [{
        type: String,
        required: false,
        default: ""
    }],
    flood: { //ativado == true || desativado == false
        type: Boolean,
        required: false,
        default: false
    },
    link : { //ativado == true || desativado == false
        type: Boolean,
        required: false,
        default: false
    },
    linkList: [{
        type: String,
        require: false,
        default: ""
    }],
    spamcaps: { //ativado == true || desativado == false
        type: Boolean,
        required: false,
        default: false
    },
    nomeAutoRole: {
        type: String,
        required: false,
        default: ""
    },
    tempoAutoRole: {
        type: Number,
        required: false,
        default: 0
    },
});

module.exports = mongoose.model('Guild', schema);