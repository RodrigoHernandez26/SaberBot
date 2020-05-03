const jwt = require('jsonwebtoken');

exports.generateToken = async (data) =>{
    return jwt.sign(data, global.SALT_KEY);
}

exports.decodeToken = async (token) => {
    var data = await jwt.verify(token, global.SALT_KEY);
    return data;
}

exports.authorize = function (req, res, next){
    var token = req.headers['x-access-token'];

    if (!token) {
        res.status(401).json({
            message: 'Acesso Restrito'
        });
    } else {
        jwt.verify(token, global.SALT_KEY, function (error, decoded) {
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

// quando entra em /dashboard/ gera um token com o access token que é valido por 2h
// todos os post, get, put e delete precisam desse token e ele é validado
// quando o token expira é necessário logar novamente