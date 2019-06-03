# -*- coding:utf-8

from flask import Flask, url_for, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

# 路由规则：
# (1) /user/<username> => type(username) == str
@app.route('/user/<username>')
def index(username):
    print(type(username))
    return username

# (2) /post/<int:id> => id = int(id)
@app.route('/post/<int:id>')
def post(id):
    print(type(id))
    return str(id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('POST')
        return 'POST'
    else:
        print('GET')
        return 'GET'

# 唯一URL重定向，路由'/hello/'可以将'/hello'的访问重定向过来
# 而路由'/hello'则不会接受'/hello/'的路由而返回404错误
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    # flask自动到/templates/目录下寻找文件返回
    return render_template('hello1.html', name=name)

# if __name__ == '__main__':
    # 可以尝试公网监听，参数host='0.0.0.0'
    # debug=True，调试模式，可以在修改代码后自动重启服务（热启动）
    # 提示中的PIN码可以用来在网页上调试
    # app.run(debug=True)

    # app.test_request_context()提供测试环境
    # url_for()使用路由的函数（def后面的函数名）创建路由
    # with app.test_request_context():
    #     print(url_for('static', filename='1.js')) # /static/1.js静态文件专用路由构造
    #     print(url_for('post', id=3)) # /post/3
    #     print(url_for('hello_world')) # /
    #     print(url_for('hello_world', tt='aa')) # /?tt=aa

with app.test_request_context('/login', method='POST'):
    print(request.path)
    print(request.method)