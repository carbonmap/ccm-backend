from flask_dotenv import DotEnv
from os import path

class Config(object):
    DEBUG = False

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        env_file_path = path.join(path.dirname(path.abspath(__file__)), '.env')
        env.init_app(app, env_file=env_file_path, verbose_mode=True)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}