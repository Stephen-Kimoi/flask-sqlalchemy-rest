# install pienv using the command "pip3 install pipenv" 
# create a Pipfile using the command "pipenv shell"
# install the dependencies flask, flask-sqlalchemy, flask-marshmallow, marshmallow-sqlalchemy 

from crypt import methods
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  
import os 

# init app 
app = Flask(__name__) 
basedir = os.path.abspath(os.path.dirname(__file__))

# Database 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite") 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# Init db 
db = SQLAlchemy(app) 
ma = Marshmallow(app) 

# Product class/model 
class Product(db.Model): 
    id = db.Column(db.Integer(), primary_key=True) 
    name = db.Column(db.String(100), unique=True) 
    description = db.Column(db.String(200)) 
    price = db.Column(db.Float) 
    quantity = db.Column(db.Integer)
    
    def __init__(self, name, description, price, quantity): 
        self.name = name 
        self.description = description 
        self.price = price 
        self.quantity = quantity

# Product schema 
class ProductSchema(ma.Schema): 
    class Meta: 
        fields = ('id', 'name', 'description', 'price', 'quantity') 

# Init schema 
product_schema = ProductSchema(strict=True) 
products_schema = ProductSchema(many=True, strict=True)

# Create a product 
@app.route('/product', methods=['POST'])
def add_product(): 
    name = request.jsonify['name']
    description = request.jsonify['description']
    price = request.jsonify['price']
    quantity = request.jsonify['quantity']

    new_product = Product(name, description, price, quantity) 

    db.session.add(new_product) 
    db.session.commit() 

    return product_schema.jsonify(new_product)

# Get a product 
@app.route('/product', methods=['GET']) 
def get_products(): 
    all_products = Product.query.all()
    result = products_schema.dump(all_products) 
    return jsonify(result.data) 

# Get single product 
@app.route('/product/<id>', methods=['GET']) 
def get_product(id): 
    product = Product.query.get(id) 
    return product_schema.jsonify(product) 

# Update a product 
@app.route('/product/<id>', methods=['PUT']) 
def update_product(id): 
    product = Product.query.get(id) 

    name = request.json['name'] 
    description = request.json['description'] 
    price = request.json['price'] 
    quantity = request.json['quantity'] 
    
    product.name = name 
    product.description = description 
    product.price = price 
    product.quantity = quantity

    db.session.commit() 

    return product_schema.jsonify(product)

# Delete product 
@app.route('/product/<id>', methods=['DELETE']) 
def delete_product(id): 
    product = Product.query.get(id) 
    db.session.delete(product) 
    db.session.commit() 

    return product_schema.jsonify(product)


# Run server 
if __name__ == '__main__': 
    app.run(debug=True) 
