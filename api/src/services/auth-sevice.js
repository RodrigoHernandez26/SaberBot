const jwt = require('jsonwebtoken');
const key = require('../settings')

exports.generateToken = (data) => {
    return jwt.sign(data, key.AUTHENTICATE_KEY, { expiresIn: '2h' });
}

exports.decodeToken = (token) => {
    return jwt.verify(token, key.AUTHENTICATE_KEY);
}

exports.authorize = function (req, res, next){
    var token = req.body['x-access-token'];

    if (!token) {
        res.status(401).json({
            message: 'Acesso Restrito'
        });
    } else {
        jwt.verify(token, key.AUTHENTICATE_KEY, function (error, decoded) {
            if (error) {
                res.status(401).json({
                    message: 'Token Inválido'
                });
            } else {
                next();
            }
        });
    }
};