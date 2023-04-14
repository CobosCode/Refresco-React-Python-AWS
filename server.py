from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import boto3
import os

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<host>/<database>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['S3_BUCKET'] = '<your-bucket-name>'
app.config['S3_ACCESS_KEY'] = '<your-access-key>'
app.config['S3_SECRET_KEY'] = '<your-secret-key>'
CORS(app)

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

    def __init__(self, name, description, image_url):
        self.name = name
        self.description = description
        self.image_url = image_url

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url
        }

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])

@app.route('/api/items', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    s3 = boto3.client('s3', aws_access_key_id=app.config['S3_ACCESS_KEY'], aws_secret_access_key=app.config['S3_SECRET_KEY'])
    s3.upload_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), app.config['S3_BUCKET'], filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_url = f'https://{app.config["S3_BUCKET"]}.s3.amazonaws.com/{filename}'
    item = Item(name, description, image_url)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize())

if __name__ == '__main__':
    app.run(debug=True)
