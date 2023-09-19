import pymysql
from sqlalchemy import create_engine, text
import sys
sys.path.append("..")
from config import mysql

# 替换为实际的数据库连接信息
db_config = mysql.Db["db1"]

# 创建数据库连接
db_connection = pymysql.connect(
    host     = db_config.host,
    user     = db_config.user,
    password = db_config.password,
    database = db_config.database,
    # db = db_config['database']
    # cahrset = db_config['charset']
)

# 创建 SQLAlchemy 引擎
engine = create_engine(
    f"mysql+pymysql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}"
)

# 设置最大空闲连接数和最大打开连接数
engine.pool._max_idle = db_config.max_idle  # 空闲连接数上限
engine.pool._max_overflow = db_config.max_open  # 最大打开连接数上限

engine.echo = db_config.show_sql
engine.execution_options(show_execution_time=db_config.show_exec_time)

if __name__ == '__main__':
    # Test
    connection = engine.connect()
    sql_query = text("SELECT * FROM users")
    # 执行 SQL 查询
    result = connection.execute(sql_query)
    # 获取查询结果
    for row in result:
        print(row)
    # 关闭结果集
    result.close()
    pass
