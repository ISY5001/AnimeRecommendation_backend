# AnimeRecommendation

# user-guide(coding)

```bash
source ~/<your_path>/myenv/bin/activate
python run.py
```

# project arch
```bash
project_name/
│
├── app/
│   ├── __init__.py
│   ├── routes/             # 存放路由处理函数
│   │   ├── __init__.py
│   │   ├── auth.py         # 认证相关路由
│   │   ├── api.py          # API 路由
│   │   ├── user.py         # 用户相关路由
│   │   └── ...
│   ├── models/             # 存放 SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py         # 用户模型
│   │   ├── post.py         # 文章/帖子模型
│   │   └── ...
│   ├── services/           # 存放业务逻辑处理函数
│   │   ├── __init__.py
│   │   ├── auth_service.py # 认证相关业务逻辑
│   │   ├── user_service.py # 用户相关业务逻辑
│   │   └── ...
│   ├── templates/          # 存放 HTML 模板文件
│   └── static/             # 存放静态文件（CSS、JavaScript、图片等）
│
├── config/
│   ├── __init__.py
│   ├── config.py          # 项目配置文件
│   └── secrets.py         # 存放敏感信息（如数据库密码、密钥等）
│
├── migrations/             # 存放数据库迁移文件（如果使用 Flask-Migrate）
│
├── tests/                  # 存放单元测试文件
│
├── venv/                   # Python 虚拟环境
│
├── .env                    # 环境变量文件
├── .gitignore              # Git 忽略文件配置
├── README.md               # 项目文档
├── requirements.txt        # 项目依赖包列表
└── run.py                  # 启动应用的入口文件
```
