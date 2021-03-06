from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

DATABASE_URL = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(100), unique=False)

    def __init__(self, image_url ):
        self.image_url = image_url


class ImageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'image_url')


image_schema = ImageSchema()
images_schema = ImageSchema(many=True)

# Endpoint to create a new image url
@app.route('/image', methods=["POST"])
def add_image():
    image_url = request.json['image_url']

    new_image = Image(image_url)

    db.session.add(new_image)
    db.session.commit()

    image = Image.query.get(new_image.id)

    return image_schema.jsonify(image)


# Endpoint to query all image urls
@app.route("/images", methods=["GET"])
def get_images():
    all_images = Image.query.all()
    result = images_schema.dump(all_images)
    return jsonify(result)


# Endpoint for querying a single image url
@app.route("/image/<id>", methods=["GET"])
def get_image(id):
    image = Image.query.get(id)
    return image_schema.jsonify(image)


# Endpoint for updating an image url
@app.route("/image/<id>", methods=["PUT"])
def image_update(id):
    image = Image.query.get(id)
    image_url = request.json['image_url']

    image.image_url = image_url

    db.session.commit()
    return image_schema.jsonify(image)


# Endpoint for deleting an image url
@app.route("/image/<id>", methods=["DELETE"])
def image_delete(id):
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()

    return "Image url was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)