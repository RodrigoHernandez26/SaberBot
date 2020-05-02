const mongoose = require('mongoose');
const Product = mongoose.model('Product');
const ValidationContract = require('../validators/fluent-validator')

exports.get = (req, res, next) => {
    Product.find({}).then(data => {
        res.status(201).send(data);
    }).catch(e => {
        res.status(400).send(e);
    })
};

exports.post = (req, res, next) => {
    let contract = new ValidationContract();
    contract.hasMinLen(req.body.title, 3, 'O título deve conter pelo menos 3 caracteres')
    contract.hasMinLen(req.body.slug, 3, 'O slug deve conter pelo menos 3 caracteres')
    contract.hasMinLen(req.body.description, 3, 'A descrição deve conter pelo menos 3 caracteres')

    if (!contract.isValid()){
        res.status(400).send({ message: "Erro!", data: e});
        return;
    }

    var product = new Product(req.body);
    product.save().then(x => {
        res.status(201).send({ message: "Produto cadastrado com sucesso!"});
    })//.catch(e => {
        //res.status(400).send({ message: "Erro!", data: e});
    //});
};

exports.put = (req, res, next) => {
    Product.findByIdAndUpdate(req.params.id, {
        $set: {
            title: req.body.title,
            description: req.body.description,
            price: req.body.price
        }
    }).then(data => {
        res.status(200).send({ message: "Produto atualizado com sucesso!"});
    }).catch(e => {
        res.status(400).send(e);
    })
};

exports.delete = (req, res, next) => {
    Product.findOneAndRemove(req.params.id).then(x => {
        res.status(201).send({message: "Produto removido com sucesso!"});
    }).catch(e => {
        res.status(400).send(e);
    })
};

//req.body => no json
//req.params => na url