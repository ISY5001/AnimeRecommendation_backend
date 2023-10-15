import yaml
import os
from flask_mysqldb import MySQL

def load_config():
    current_directory = os.getcwd()
    config_file_path = os.path.join(current_directory, 'config', 'config.yaml')
    with open(config_file_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def configure_mysql(app, mysql_config):
    app.config['MYSQL_HOST'] = mysql_config['host']
    app.config['MYSQL_USER'] = mysql_config['user']
    app.config['MYSQL_PASSWORD'] = mysql_config['password']
    app.config['MYSQL_DB'] = mysql_config['db']
    app.config['SECRET_KEY'] = mysql_config['secret_key']
    mysql = MySQL(app)
    return mysql