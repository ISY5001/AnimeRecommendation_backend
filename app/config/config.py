import threading

class Config:
    def __init__(self):
        # self.Language = ""
        # self.Token = ""
        # self.Super = ""
        # self.RedisPre = ""
        self.Host = ""
        # self.OpenJwt = False
        self.Routes = []

Cfg = Config()
mutex = threading.Lock()
declare = threading.Event()

def set_config(cfg):
    global Cfg
    mutex.acquire()
    try:
        # Cfg.RedisPre = set_default(cfg.RedisPre, "", "go.sso.redis")
        Cfg.Language = set_default(cfg.Language, "", "cn")
        Cfg.Token = set_default(cfg.Token, "", "token")
        Cfg.Super = set_default(cfg.Super, "", "admin")  # 超级账户
        Cfg.Host = set_default(cfg.Host, "", "http://localhost:8282")  # 域名
        Cfg.Routes = cfg.Routes
        # Cfg.OpenJwt = cfg.OpenJwt
    finally:
        mutex.release()

def set_default(value, default, default_value):
    if value == default:
        return default_value
    return value
