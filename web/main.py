# -*- coding:utf-8
from flask import Flask
from app import admin, search
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(search, url_prefix='/search')
app.secret_key = '123456'
# 显示模板加载
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

if __name__ == '__main__':
    app.run(debug=True)
