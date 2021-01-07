import os
from project import create_app

config_settings = os.environ.get("APP_CONFIG_SETTINGS", "development.cfg")

app = create_app(config_settings)

# # IF RUNNING ON PYCHARM:
# if __name__ == '__main__':
#     app.run()
