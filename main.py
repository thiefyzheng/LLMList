# server.py
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
db = SQLAlchemy(app)

class Model(db.Model):
    _id = db.Column(db.String, primary_key=True)
    id = db.Column(db.String)
    likes = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    downloads = db.Column(db.Integer)
    tags = db.Column(db.String)
    createdAt = db.Column(db.String)
    modelId = db.Column(db.String)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models')
def get_models():
    models = Model.query.with_entities(Model.id).limit(10).all()
    return jsonify([model.id for model in models])

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
