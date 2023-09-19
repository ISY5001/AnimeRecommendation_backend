# class DbConfig:
#     def __init__(self, driver_name, dsn, show_sql, show_exec_time, max_idle, max_open):
#         self.driver_name = driver_name
#         self.dsn = dsn
#         self.show_sql = show_sql
#         self.show_exec_time = show_exec_time
#         self.max_idle = max_idle
#         self.max_open = max_open

class DbConfig:
    def __init__(self, host_name, user_name, password, database_name, show_sql, show_exec_time, max_idle, max_open):
        self.host = host_name
        self.user = user_name
        self.password = password
        self.database = database_name
        self.show_sql = show_sql
        self.show_exec_time = show_exec_time
        self.max_idle = max_idle
        self.max_open = max_open

# 创建数据库配置字典
Db = {
    "db1": DbConfig(
        host_name="localhost",
        user_name="dev",
        password="dev",
        database_name="irs_user",
        # driver_name="mysql",
        # dsn="mysql+pymysql://dev:dev@127.0.0.1:3306/irs_user?charset=utf8mb4&parseTime=true&loc=Local",
        show_sql=True,
        show_exec_time=False,
        max_idle=10,
        max_open=200
    )
}
