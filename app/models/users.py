from datetime import datetime
from pymysql import cursors
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import engine

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    # Ctime = Column(Integer, default=0, nullable=False, comment='创建时间', index=True)
    # Email = Column(String(100), default='', nullable=False, comment='邮箱')
    # Ext = Column(Text, nullable=False, comment='扩展字段')
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键')
    # Mtime = Column(TIMESTAMP, default=datetime.utcnow, nullable=False, comment='修改时间')
    Name = Column(String(50), default='', nullable=False, comment='用户名')
    Passwd = Column(String(50), nullable=False, comment='密码')
    # Mobile = Column(String(20), default='', nullable=False, comment='手机号')
    # Salt = Column(String(4), nullable=False, comment='盐值')
    # Status = Column(Integer, default=0, nullable=False, comment='状态（0：未审核,1:通过 10删除）')

class UserRow():
    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键')
    Name = Column(String(50), default='', nullable=False, comment='用户名')
    # Email = Column(String(100), default='', nullable=False, comment='邮箱')
    # Mobile = Column(String(20), default='', nullable=False, comment='手机号')

# UsersStatusOk = 1
# UsersStatusDel = 10
# UsersStatusDef = 0

usersTable = "users"

# 创建数据库连接和 session
Session = sessionmaker(bind=engine)
session = Session()

# 获取单个用户记录
def get_user_row_by_id(user_id):
    # user_row = session.query(UserRow).filter_by(Id=user_id).first()
    # return user_row
    user_row = session.query(Users).filter_by(Id=user_id).first()
    if user_row:
        user_data = {
            "Id": user_row.Id,
            "Name": user_row.Name
            # anyother value
        }
        return user_data
    else:
        return None

# # 检查手机号是否存在
# def is_exists_mobile(mobile):
#     user = session.query(Users).filter_by(Mobile=mobile).first()
#     return user is not None

# 添加用户
# def add_user(user, trace, device):
def add_user(user):
    session.add(user)
    # session.add(trace)
    # session.add(device)
    session.commit()

# 获取所有用户
def get_all_users():
    users = session.query(Users).all()
    return users

# 获取单个用户
def get_user_by_id(user_id):
    user = session.query(Users).filter_by(Id=user_id).first()
    return user

if __name__ == '__main__':
    # Without Testing
    # Base.metadata.create_all(engine)
    # Base = declarative_base()

    # Test 1
    user_data = get_user_row_by_id(1)
    if user_data:
        print("User Data:")
        print(f"ID: {user_data['Id']}")
        print(f"Name: {user_data['Name']}")
    else:
        print("User not found")

    # Test 2
    user_datas = get_all_users()
    for udata in user_datas:
        print(udata['Id'])