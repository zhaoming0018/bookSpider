from flask import Blueprint

# 一个公用蓝图
admin = Blueprint('admin', __name__, template_folder='templates')