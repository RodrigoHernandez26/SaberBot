const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const schema = new Schema({
    guildID: {
        type: Number,
        required: true,
        unique: true
    },
    limAdd: {
        type: Number,
        required: false,
        default: 10
    },
    limQnt: {
        type: Number,
        required: false,
        default: 30
    },
    limDado: {
        type: Number,
        required: false,
        default: 100
    },
    addLim: {
        type: Number,
        required: false,
        default: 10
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
        type: Number,
        required: false
    }],
    chatsDisableMsg:{ //aviso == false || deletar == true
        type: Boolean,
        required: false,
        default: false
    },
    admRoles: [{
        type: Number,
        required: false
    }],
    numMute: {
        type: Number,
        required: false,
        default: 3
    },
    numKick: {
        type: Number,
        required: false,
        default: 5
    },
    numBan: {
        type: Number,
        required: false,
        default: 12
    },
    tempoMute: { //segundos
        type: Number,
        required: false,
        default: 3600
    },
    tempoBan: { //segundos
        type: Number,
        required: false,
        default: 3600
    },
    tempoAviso: { //segundos
        type: Number,
        required: false,
        default: 3600
    },
    localMsgAviso: { //"dm" == true || "chat" == false
        type: Boolean,
        required: false,
        default: false
    },
    idAviso: {
        type: Number,
        required: false,
        default: 0
    },
    autoBan: {
        type: Boolean,
        required: false,
        default: false
    },
    banWords: [{
        type: String,
        required: false,
        default: ""
    }],
    tempoAutoRole: {
        type: Number,
        required: false,
        default: 0
    },
    autoRoleMsg: {
        type: Boolean,
        required: false,
        default: false
    }
});

module.exports = mongoose.model('Guild', schema);