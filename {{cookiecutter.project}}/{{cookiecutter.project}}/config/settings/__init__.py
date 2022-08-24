import importlib
import yaml
from {{cookiecutter.project}}.config.settings.base_settings import *
from {{cookiecutter.project}}.utils import update_config_recursively


def load_env(env_file_path='/etc/{{cookiecutter.project}}/env.yaml'):
    app_env = os.environ.get('APP_ENV')
    if app_env:
        return app_env

    if os.path.isfile(env_file_path):
        with open(env_file_path) as f:
            config = yaml.safe_load(f)
            app_env = config.get('APP_ENV')
    if app_env:
        return app_env
    return 'dev'


def load_env_settings(env):
    # 读取配置
    dir_name = os.path.dirname(__file__)
    env_setting_path = os.path.join(dir_name, env, 'settings.yaml')
    with open(env_setting_path) as f:
        env_config = yaml.safe_load(f)

    # 加载
    global_vars = globals()
    for k, v in env_config.items():
        if isinstance(global_vars.get(k), dict):
            update_config_recursively(global_vars[k], v)
        else:
            global_vars[k] = v


current_env = load_env()

load_env_settings(current_env)

print("loading %s" % current_env)

ret = importlib.import_module("{{cookiecutter.project}}.config.settings.%s.logger" % current_env)
LOGGING = ret.LOGGING

