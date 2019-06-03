from flask import request, render_template, redirect
from flask_paginate import Pagination
from app.admin.tool import login_required
from app.admin.blue import admin
from models.BookModel import BookModel

# 图书列表页
@admin.route('/book/list/', methods=['GET', 'POST'])
@login_required
def book_list():
    page = int(request.args.get('page', 1))
    bookModel = BookModel()
    con = {}
    con['bookname'] = request.args.get('bookname', '')
    con['author'] = request.args.get('author', '')
    con['order'] = request.args.get('order', '')
    books, count = bookModel.find(page_num=page, condition=con)
    page_obj = Pagination(page=page, total=int(count)//20, per_page_count=20, bs_version='3')
    html = page_obj.links
    return render_template('admin/bookList.html', books=books, pageinfo=html, func='book')

# 删除书
@admin.route('/book/delete/<int:id>')
def delete_book(id):
    bookModel = BookModel()
    bookModel.delete(id)
    return redirect('admin/book/list/')

# 查看书
@admin.route('/book/view')
@login_required
def book_view():
    id = request.args.get('id', None)
    bookModel = BookModel()
    bookInfo = bookModel.getInfo(id)
    return render_template('admin/book_view.html', book=bookInfo, func='book')

# 更改书信息
@admin.route('/book/change/<int:id>', methods=['GET','POST'])
@login_required
def book_change(id):
    bookModel = BookModel()
    bookModel.update(id, request.form)
    return redirect('/admin/book/view?id='+str(id))

# 增加书
@admin.route('/book/add', methods=['GET', 'POST'])
@login_required
def book_add():
    if request.method == 'POST':
        bookModel = BookModel()
        if bookModel.add(request.form):
            return redirect('/admin/book/list/')
    return render_template('admin/book_add.html', func='book')
