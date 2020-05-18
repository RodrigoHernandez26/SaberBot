const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const settings = require('./settings')

const app = express();
const router = express.Router();

// Connect DB
mongoose.set('useCreateIndex', true);
mongoose.connect(settings.connectionStrig, { useNewUrlParser: true, useUnifiedTopology: true })

//Models
const Guild = require('./models/guild-model');

//Rote
const guildRoute = require('./routes/guild-route');

app.use(bodyParser.json());
app.unsubscribe(bodyParser.urlencoded({ extended: false }));

app.use('/', guildRoute);

module.exports = app;