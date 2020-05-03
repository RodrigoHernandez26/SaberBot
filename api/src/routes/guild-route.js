const express = require('express');
const router = express.Router();
const controller = require('../controllers/guild-controller');
const authService = require('../services/auth-sevice');


router.get('/guild', authService.authorize,controller.getGuild)
router.post('/guild', authService.authorize, controller.postGuild)
router.put('/guild', authService.authorize, controller.putGuild)
router.delete('/guild', authService.authorize, controller.deleteGuild)
router.post('/token', controller.postToken)

module.exports = router;