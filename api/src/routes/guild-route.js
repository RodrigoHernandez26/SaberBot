const express = require('express');
const router = express.Router();
const controller = require('../controllers/guild-controller');
const authService = require('../services/auth-sevice');


router.post('/guild/data', authService.authorize, controller.getGuilds)
router.post('/guild/get', authService.authorize, controller.guildid)
router.post('/guild/sign', authService.authorize, controller.postGuild)
// router.put('/guild', authService.authorize, controller.putGuild)
router.delete('/guild/delete', authService.authorize, controller.deleteGuild)
router.post('/token', controller.postToken)
router.post('/data', authService.authorize, controller.postData)

module.exports = router;