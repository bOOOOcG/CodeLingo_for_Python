# module/config_manager.py

import json
import os
import zlib
import base64
from cryptography.fernet import Fernet
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  # 创建logger

class ConfigManager:
    DEFAULT_CONFIG = {
        "General": {
            "show_console_log": False
        },
        "Visual": {
            "light_mode": False  # 新的配置项作为 Visual 的子键
        }
    }
    CONFIG_FILE = "config.cfg"  # 配置文件的名称
    KEY = "wq_oPbG6IYY0APUmDnxw9gy5zGDtM4D9V-vcuFW0Zwo="
    fernet = Fernet(KEY)

    def __init__(self, allow_plain_text=True):
        self.allow_plain_text = allow_plain_text
        self.config = self.load_config()

    def encrypt_config(self, config_data):
        # 最小化JSON数据
        minified_json = json.dumps(config_data, separators=(',', ':')).encode()
        # 压缩数据
        compressed = zlib.compress(minified_json)
        # 加密
        encrypted = self.fernet.encrypt(compressed)
        return encrypted

    def decrypt_config(self, encrypted_data):
        try:
            # 解密
            decrypted = self.fernet.decrypt(encrypted_data)
            # 解压数据
            decompressed = zlib.decompress(decrypted)
            # 转换回字典
            config_data = json.loads(decompressed.decode())
            return config_data
        except Exception as e:
            logger.error(f"解密配置文件失败：{str(e)}")
            if self.allow_plain_text:
                try:
                    config_data = json.loads(encrypted_data.decode())
                    return config_data
                except json.JSONDecodeError:
                    logger.error("配置文件格式错误，无法读取。")
            return None

    def load_config(self):
        if not os.path.exists(self.CONFIG_FILE):
            logger.info("配置文件不存在，正在创建默认配置文件。")
            self.create_default_config()
            # 加载刚创建的默认配置
            with open(self.CONFIG_FILE, 'rb') as file:
                config_data = file.read()
            config = self.decrypt_config(config_data)
        else:
            with open(self.CONFIG_FILE, 'rb') as file:
                config_data = file.read()

            config = self.decrypt_config(config_data)
            if config is None:
                logger.warning("未使用加密或解密失败，且不允许使用明文配置。使用默认配置。")
                config = self.DEFAULT_CONFIG

        return config

    def save_config(self, config=None):
        if config is None:
            config = self.config

        if self.allow_plain_text:
            config_data = json.dumps(config).encode()
            logger.debug("以明文形式保存配置文件。")
        else:
            config_data = self.encrypt_config(config)
            logger.debug("以加密形式保存配置文件。")

        with open(self.CONFIG_FILE, 'wb') as file:
            file.write(config_data)
        logger.info("配置文件已保存。")

    def update_setting(self, setting, value):
        self.config[setting] = value
        self.save_config()  # 保存更改
        logger.debug(f"配置项'{setting}'已更新。")

    def get_setting(self, key, default=None):
        logging.debug(f"Getting setting for key: {key}")
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            logging.debug(f"Found setting for key {key}: {value}")
            return value
        except KeyError:
            logging.debug(f"Setting for key {key} not found, returning default: {default}")
            return default

    def create_default_config(self):
        default_config = self.DEFAULT_CONFIG.copy()  # 创建默认配置的副本
        with open(self.CONFIG_FILE, 'wb') as file:
            config_data = self.encrypt_config(default_config)
            file.write(config_data)
        logger.info("默认配置文件已创建。")
