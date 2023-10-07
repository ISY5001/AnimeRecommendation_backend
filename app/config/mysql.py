# class DbConfig:
#     def __init__(self, driver_name, dsn, show_sql, show_exec_time, max_idle, max_open):
#         self.driver_name = driver_name
#         self.dsn = dsn
#         self.show_sql = show_sql
#         self.show_exec_time = show_exec_time
#         self.max_idle = max_idle
#         self.max_open = max_open

# class DbConfig:
#     def __init__(self, host_name, user_name, password, database_name, show_sql, show_exec_time, max_idle, max_open):
#         self.host = host_name
#         self.username = user_name
#         self.password = password
#         self.database = database_name
#         self.show_sql = show_sql

# # 创建数据库配置字典
# Db = {
#     "db1": DbConfig(
#         host_name="localhost",
#         user_name="dev",
#         password="dev",
#         database_name="userdata",
#         show_sql=True,
#         # show_exec_time=False,
#         # max_idle=10,
#         # max_open=200
#     )
# }
# mysql_config.py

from flask_mysqldb import MySQL

def configure_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_DB'] = 'user_data'
    app.config['SECRET_KEY'] = 'afhfhkgigugh'
    mysql = MySQL(app)
    return mysql
