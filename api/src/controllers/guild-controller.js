const mongoose = require('mongoose');
const Guild = mongoose.model('Guild');
const jwt = require('../services/auth-sevice')

exports.postToken = (req, res, next) => {
    res.status(200).json({token: jwt.generateToken(req.body)});
}

exports.postData = (req, res, next) => {
    res.status(200).send({data: jwt.decodeToken(req.body['x-access-token'])});
}

exports.getGuild = (req, res, next) => {

    const data = jwt.decodeToken(req.body['x-access-token'])

    for (var i = 0; i < data['user_guilds'].length; i++){
        if (req.body.guildID == data['user_guilds'][i]['id']){
            Guild.find({
                guildID: req.body.guildID
            }).then(data => {
                res.status(201).send(data);
            }).catch(e => {
                res.status(400).send(e);
            })
            return;
        }
    }
    res.status(400).send({ message : "Acesso Negado" })
};

exports.postGuild = (req, res, next) => {
    let guild = new Guild(req.body);
    guild.save().then(x => {
        res.status(201).send({ message: "Server cadastrado com sucesso!"});
    }).catch(e => {
        res.status(400).send({ message: "Erro!", data: e});
    });
};

// exports.putGuild = (req, res, next) => {
//     Guild.replaceOne({guildID: req.body.guildID}, req.body)
//     .then(data => {
//         res.status(200).send({ message: "Server atualizado com sucesso!", data: req.body});
//     }).catch(e => {
//         res.status(400).send(e);
//     })
// };

exports.deleteGuild = (req, res, next) => {
    Guild.deleteOne({guildID: req.body.guildID})
    .then(x => {
        res.status(201).send({message: "Server removido com sucesso!"});
    }).catch(e => {
        res.status(400).send(e);
    })
};