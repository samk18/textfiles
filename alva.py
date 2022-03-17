	from email.policy import default
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from datetime import datetime
import psycopg2
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  account_id = db.Column(db.String(100), unique=True)
  amount = db.Column(db.Integer)
  date_created = db.column(db.DateTime)

  def __init__(self, account_id, amount):
    self.account_id = account_id
    self.amount = amount

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'account_id', 'amount', 'date_created')

# Init schema
product_schema = ProductSchema(many=False)
products_schema = ProductSchema(many=True)

@app.route("/ping")
def health():
  #  db.engine.execute('SELECT 1')

    return "The service is up and running."

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  account_id = request.json['account_id']
  amount = request.json['amount']

  new_product = Product(account_id, amount)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result.data)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)