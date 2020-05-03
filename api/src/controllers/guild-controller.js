const mongoose = require('mongoose');
const Guild = mongoose.model('Guild');
const authService = require('../services/auth-sevice')

exports.postToken = async (req, res, next) => {
    res.status(200).json({token: await authService.generateToken(req.body.access_token)});
}

exports.getGuild = (req, res, next) => {
    Guild.find({
        guildID: req.body.guildID
    }).then(data => {
        res.status(201).send(data);
    }).catch(e => {
        res.status(400).send(e);
    })
};

exports.postGuild = (req, res, next) => {
    let guild = new Guild(req.body);
    guild.save().then(x => {
        res.status(201).send({ message: "Server cadastrado com sucesso!"});
    }).catch(e => {
        res.status(400).send({ message: "Erro!", data: e});
    });
};

exports.putGuild = (req, res, next) => {
    Guild.replaceOne({guildID: req.body.guildID}, req.body)
    .then(data => {
        res.status(200).send({ message: "Server atualizado com sucesso!", data: req.body});
    }).catch(e => {
        res.status(400).send(e);
    })
};

exports.deleteGuild = (req, res, next) => {
    Guild.deleteOne({guildID: req.body.guildID})
    .then(x => {
        res.status(201).send({message: "Server removido com sucesso!"});
    }).catch(e => {
        res.status(400).send(e);
    })
};