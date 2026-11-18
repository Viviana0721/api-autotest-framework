# -*- coding: utf-8 -*-
"""全局 fixture：配置加载、接口实例、登录态管理。

登录态用 session 级 fixture 管理，只登录一次；后续接口通过同一个
requests.Session 自动携带 Cookie/Token，避免每个用例重复登录。
"""
import os

import pytest
import yaml

from api.post_api import PostApi
from utils.assert_util import AssertUtil

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    env = cfg.get("env", "test")
    return {
        "base_url": cfg["base_url"][env],
        "timeout": cfg.get("timeout", 10),
        "headers": cfg.get("headers", {}),
    }


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def session(config):
    """整个测试会话共用一个 Session，等价于「登录一次，全局复用」。"""
    import requests

    s = requests.Session()
    s.headers.update(config["headers"])
    yield s
    s.close()


@pytest.fixture(scope="session")
def post_api(config, session):
    api = PostApi(base_url=config["base_url"], timeout=config["timeout"])
    api.session = session
    return api


@pytest.fixture(scope="session")
def expect():
    return AssertUtil()
