from flask import session,Blueprint, Flask, request, render_template, make_response, redirect, url_for
from tools.book import getbooks, book_delete
from tools.manager import get_managers
from flask_paginate import Pagination, get_page_parameter
from app.search.tool import do_register, check_register, login_valid
from tools.book import getbooks
from .tool import login_required
from models.BookModel import BookModel
from tools.user import User

search = Blueprint('search', __name__, template_folder='templates/search')

@search.route('/index')
@login_required
def index():
    return render_template('index.html')

@search.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if login_valid(request.form['username'], request.form['passwd']):
            session['username'] = request.form['username']
            return redirect('/search/index')
    return render_template('login.html')

@search.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('search/register.html')
    if request.method == 'POST':
        error = check_register(request)
        print(error)
        if len(error) == 0:
            do_register(request)
            return redirect('/search/login')
        else:
            return render_template('register.html', error=error)

@search.route('/list')
@login_required
def book_list():
    page = int(request.args.get('page', 1))
    kind = request.args.get('type', None)
    word = request.args.get('word', None)
    condition = {}
    if kind is not None:
        condition[kind] = word
    bookModel = BookModel()
    books, count = bookModel.find(page_num=page, condition=condition)
    print(count)
    page_obj = Pagination(page=page, total=int(count)//20, per_page_count=20, bs_version='3')
    html = page_obj.links
    return render_template('book_list.html', books=books, html=html)

@search.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    user = User()
    userInfo = user.getUserByName(session['username'])
    if request.method == 'POST':
        print(request.form)
        user.modify(userInfo['id'], request.form)
    return render_template('profile.html', userInfo=userInfo)