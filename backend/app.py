from flask import Flask, jsonify, request
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import pymysql
import os
from dotenv import load_dotenv
import pytz

load_dotenv() 


pymysql.install_as_MySQLdb()

app = flask.Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
# 'mysql+pymysql://root:pass1478@localhost/flask?unix_socket=/opt/lampp/var/mysql/mysql.sock'



app.config['SQLALCHEMY_DATABASE_URI'] = \
f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

def get_bd_time():
    bd_tz = pytz.timezone('Asia/Dhaka')
    return datetime.now(bd_tz) 

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date =  db.Column(db.DateTime, default=get_bd_time)


    def __init__(self, title, body):
        self.title = title
        self.body = body


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Articles
        Load_instance = True
    id = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
    date = ma.auto_field()



article_schema = ArticleSchema()
article_schemas = ArticleSchema(many=True)


@app.route("/get", methods=["GET"])
def get_articles():
    all_articles = Articles.query.all()
    result = article_schemas.dump(all_articles)
    return jsonify(result)


@app.route("/get/<int:id>/", methods=["GET"])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

@app.route("/update/<int:id>/", methods=["PUT"])
def update_article(id):
    data = flask.request.get_json()
    if not data:
        return {"error": "No JSON data received"}, 400

    # SQLAlchemy 2.0 compatible way
    article = db.session.get(Articles, id)
    if not article:
        return {"error": "Article not found"}, 404

    article.title = data.get("title", article.title)
    article.body = data.get("body", article.body)
    db.session.commit()

    return article_schema.jsonify(article)


@app.route("/add", methods=["POST"])
def add_article():
    title = flask.request.json["title"]
    body = flask.request.json["body"]
    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route("/delete/<int:id>/", methods=["DELETE"])
def delete_article(id):
    article = Articles.query.get(id)
    if not article:
        return {"error": "Article not found"}, 404
    db.session.delete(article)
    db.session.commit()
    return {"message": "Article deleted successfully"}

from flask_cors import CORS
CORS(app,origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5001"])  # enable for all routes


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(host="0.0.0.0", port=5000)
   
