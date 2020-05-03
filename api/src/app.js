const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const settings = require('./settings')

const app = express();
const router = express.Router();

// Connect DB
mongoose.connect(settings.connectionStrig)

//Models
const Guild = require('./models/guild-model');

//Rote
const guildRoute = require('./routes/guild-route');

app.use(bodyParser.json());
app.unsubscribe(bodyParser.urlencoded({ extended: false }));

app.use('/guild', guildRoute);

module.exports = app;

//Get pega as configurações do site e configura o bot
//Post pega as configurações do bot e mostra no site
