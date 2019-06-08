## 图书搜索管理系统

---

1. 使用flask构建，数据库基于mysql，使用pymysql做连接；

2. 请导入bookdb.sql，会加载一个testbook数据库，如果已有不用增加；

2. 分页依赖：flask-paginate；

3. 启动： 运行python main.py；

4. 项目分前端后台，以下为显示页面的路由：
    后台登录 /admin/login
    前台登录 /search/login