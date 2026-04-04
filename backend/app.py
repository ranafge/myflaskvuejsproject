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

# DB_USER= os.getenv('DB_USER', 'root')
# DB_PASSWORD= os.getenv('DB_PASSWORD', 'pass1478')
# DB_HOST= os.getenv('DB_HOST', 'localhost')
# DB_NAME= os.getenv('DB_NAME', 'flask')

IS_KUBERNETES = os.getenv('KUBERNETES', 'false').lower() == 'true'

if IS_KUBERNETES:
    # Kubernetes ক্লাস্টারের ভেতরে
    DB_HOST = os.getenv('DB_HOST', 'mysql-service')
    DB_USER = os.getenv('DB_USER', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass1478')
    DB_NAME = os.getenv('DB_NAME', 'flask')
else:
    # লোকাল ডেভেলপমেন্ট
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass1478')
    DB_NAME = os.getenv('DB_NAME', 'flask')


# app.config['SQLALCHEMY_DATABASE_URI'] = \
# f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:pass1478@localhost/flask?unix_socket=/opt/lampp/var/mysql/mysql.sock'

print(f"🔗 Connecting to database at: {DB_HOST}")

# app.config['SQLALCHEMY_DATABASE_URI'] = \
# f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

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

@app.route("/", methods=["GET"])
def home():
    return {
        "message": "Flask api is running",
        "version": "1.0.0",
        "status": "Healthy",
        "endpoints": {
            "GET /get": "Get all articles",
            "GET /get/<id>": "Get single article",
            "POST /add": "Add new article",
            "PUT /update/<id>": "Update a article",
            "DELETE /delete/<id>": "Delete article"
        },
        "database": "Connected " if Articles else "Not connected",
        "timestamp": get_bd_time().isoformat()


    }


@app.route("/add", methods=["POST", "OPTIONS"])
@app.route("/add/", methods=["POST", "OPTIONS"])
def add_article():
    if request.method == "OPTIONS":
        return " ", 200
    data = request.get_json()
    if not data:
        return {"error": "No JSON data received"}, 400      
    title = data.get("title")
    body = data.get("body")
    if not title or not body:
        return {"error": "Title and body are required"}, 400
    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    
    return article_schema.jsonify(articles), 201


@app.route("/get", methods=["GET", "OPTIONS"])
def get_articles():
    if request.method == "OPTIONS":
         return " ", 200
    all_articles = Articles.query.all()
    result = article_schemas.dump(all_articles)
    return jsonify(result)


@app.route("/get/<int:id>", methods=["GET", "OPTIONS"])
@app.route("/get/<int:id>/", methods=["GET", "OPTIONS"])
def post_details(id):
    if request.method == "OPTIONS":
        return " ", 200
    article = Articles.query.get(id)
    return article_schema.jsonify(article)


@app.route("/update/<int:id>" , methods=["PUT", "OPTIONS"])
@app.route("/update/<int:id>/", methods=["PUT", "OPTIONS"])
def update_article(id):
    if request.method == "OPTIONS":
        return " ", 200
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





@app.route("/delete/<int:id>", methods=["DELETE", "OPTIONS"])
@app.route("/delete/<int:id>/", methods=["DELETE", "OPTIONS"])
def delete_article(id):
    if request.method == "OPTIONS":
        return " ", 200
    article = Articles.query.get(id)
    if not article:
        return {"error": "Article not found"}, 404
    db.session.delete(article)
    db.session.commit()
    return {"message": "Article deleted successfully"}


from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://app.myapp.local:8080",
            "http://app.myapp.local",
            "http://samsul.islam.rana",
            "http://192.168.0.100:5173",
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created.")
        print("App is running")
    app.run(host="0.0.0.0", port=5000)
   
