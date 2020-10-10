from flask_dotenv import DotEnv

class Config(object):
    DEBUG = False

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        env.init_app(app, verbose_mode=True)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}