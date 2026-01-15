#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if not set
    if 'page_views' not in session:
        session['page_views'] = 0
    
    # Increment page views
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check if limit exceeded (3 views allowed, 4th blocked)
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    # Query article and return as JSON
    article = Article.query.get(id)
    if article is None:
        return jsonify({'error': 'Article not found'}), 404
    return jsonify(article.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
