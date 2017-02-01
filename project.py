from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from werkzeug import secure_filename
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Book

# Imports for Session Logging
from flask import session as login_session
import random
import string

# Imports for OAUTH
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION = "Udacity Book Catalog Project"

# Connect to Database and create database session
engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON APIs to view Book Information


@app.route('/categories/<string:category_name>/JSON')
@app.route('/categories/<string:category_name>/books/JSON')
def booksJSON(category_name):
    category_id = getCategoryID(category_name)
    books = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(Books=[i.serialize for i in books])


@app.route('/books/<string:book_title>_<int:book_id>/JSON')
def bookJSON(book_title, book_id):
    editedBook = getBookInfo(book_id)
    category = getCategoryInfo(editedBook.category_id)
    return jsonify(
        editedBook=editedBook.serialize,
        category=category.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/')
@app.route('/categories')
def bookCategories():
    categories = session.query(Category).all()
    return render_template(
        'categories.html',
        categories=categories,
        login_session=login_session)


@app.route('/categories/<string:category_name>/')
@app.route('/categories/<string:category_name>/books/')

def showBooks(category_name):
    category_id = getCategoryID(category_name)
    books = session.query(Book).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicbooks.html',
            books=books,
            category_name=category_name,
            login_session=login_session)
    else:
        return render_template(
            'books.html',
            books=books,
            category_name=category_name,
            login_session=login_session)


@app.route(
    '/books/<string:book_title>_<int:book_id>/edit',
    methods=[
        'GET',
        'POST'])
def editBook(book_title, book_id):
    editedBook = getBookInfo(book_id)
    category = getCategoryInfo(editedBook.category_id)
    # import pdb; pdb.set_trace()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if login_session['userid'] != editedBook.user_id:
        return redirect(
            url_for(
                'showBooks',
                category_name=request.form['category'],
                login_session=login_session))
    else:
        if request.method == 'POST':
            if request.form['title']:
                editedBook.title = request.form['title']
            if request.form['author']:
                editedBook.author = request.form['author']
            if request.form['img']:
                editedBook.img = request.form['img']
            if request.form['category']:
                editedBook.category_id = getCategoryID(
                    request.form['category'])
            session.add(editedBook)
            session.commit()
            return redirect(
                url_for(
                    'showBooks',
                    category_name=request.form['category'],
                    login_session=login_session))
        else:
            return render_template(
                'editBook.html',
                book=editedBook,
                category_name=category.name,
                login_session=login_session)


@app.route(
    '/books/<string:book_title>_<int:book_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteBook(book_title, book_id):
    deletedBook = getBookInfo(book_id)
    category_name = getCategoryName(book_id)
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if login_session['userid'] != deletedBook.user_id:
        return redirect(
            url_for(
                'showBooks',
                category_name=request.form['category'],
                login_session=login_session))
    else:
        if request.method == 'POST':
            session.delete(deletedBook)
            return redirect(url_for('showBooks', category_name=category_name))
        else:
            return render_template(
                'deleteBook.html',
                book=deletedBook,
                category_name=category_name)


@app.route('/books/new', methods=['GET', 'POST'])
def newBooks():
    if 'username' not in login_session:
        categories = session.query(Category).all()
        return render_template(
            'categories.html',
            categories=categories,
            login_session=login_session)
    else:
        if request.method == 'POST':
            newBook = Book(
                title=request.form['title'],
                author=request.form['author'],
                img=request.form['img'],
                category_id=getCategoryID(
                    request.form['category']),
                user_id=login_session['userid'])
            session.add(newBook)
            session.commit()
            return redirect(
                url_for(
                    'showBooks',
                    category_name=request.form['category']))
        else:
            return render_template('newBook.html')


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    if getUserID(data['email']):
        user = getUserInfo(getUserID(data['email']))
        login_session['username'] = user.name
        login_session['picture'] = user.picture
        login_session['email'] = user.email
        login_session['provider'] = 'google'
        login_session['userid'] = user.id
        output = ''
        output += '<h1>Welcome back, '
    else:
        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']
        login_session['provider'] = 'google'
        login_session['userid'] = createUser(login_session)
        output = ''
        output += '<h1>Welcome, '

    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/disconnect')
def disconnect():
    access_token = login_session['credentials'].access_token
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['userid']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have successfully been logged out.")
        return redirect(url_for('bookCategories'))
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        flash("You were not logged in")
        return redirect(url_for('bookCategories'))


@app.route('/clearSession')
def clearSession():
    login_session.clear()
    return "Session cleared"

# helper functions


def getCategoryID(category_name):
    """
    Function name: getCategoryID
    Args:
        category_name (data type: str): It's the string version of the category name
    Returns:
        category.id (data type: int): The ID number for the category
    """
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        return category.id
    except:
        return None


def getCategoryInfo(category_id):
    """
    Function name: getCategoryInfo
    Args:
        category_id (data type: int): It's the string version of the category ID
    Returns:
        category (data type: Category): Returns the entire Category object
    """
    category = session.query(Category).filter_by(id=category_id).one()
    return category


def getBookInfo(book_id):
    """
    Function name: getBookInfo
    Args:
        book_id (data type: int): It's the string version of the book ID
    Returns:
        book (data type: Book): Returns the entire Book object
    """
    book = session.query(Book).filter_by(id=book_id).one()
    return book


def getCategoryName(book_id):
    """
    Function name: getCategoryName
    Args:
        book_id (data type: int): It's the int version of the book ID
    Returns:
        category.name (data type: str): Returns the string version of the category name
    """
    book = getBookInfo(book_id)
    category = getCategoryInfo(book.category_id)
    return category.name

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
