const express = require('express');
const router = express.Router()
const controller = require('../controllers/product-controller')

router.get('/', controller.get)
router.post('/', controller.post)
router.post('/:id', controller.put)
router.delete('/:id', controller.delete)
 
module.exports = router;