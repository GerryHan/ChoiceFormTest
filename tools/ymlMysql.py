import configparser
from dataclasses import dataclass

import yaml
from pathlib import Path
import logging
import logging.handlers
import os
import time

import pymysql


@dataclass
class Global:
    ROOT: str
    CONFIG: dict


class Parser(configparser.ConfigParser):
    def values(self):
        sd = dict(self._sections)
        for k in sd:
            sd[k] = dict(sd[k])
        return sd

    def conf(self, conf_file):
        if Path(conf_file).exists():
            self.read(filenames=conf_file, encoding="utf-8")
        else:
            raise FileNotFoundError(f"{conf_file}")
        return self.values()


class Yml:
    def __init__(self, file):
        if Path(file).exists():
            self.file = file
            self.yc = None
        else:
            raise FileNotFoundError

    def __getitem__(self, key: str = None):
        return str(self.yc[key]) if key in self.yc else None

    @property
    def parameters(self):
        with open(str(self.file), "rb") as yf:
            self.yc = yaml.safe_load(yf)
        return dict(self.yc)


class MySQL:
    def __init__(self, config: dict):
        self.config = config

    @property
    def db(self):
        return pymysql.connect(
            host=self.config.get("host"),
            port=int(self.config.get("port")),
            database=self.config.get("database"),
            user=self.config.get("user"),
            password=self.config.get("password"),
            charset="utf8",
            autocommit=True,
        )

    @property
    def cursor(self):
        return self.db.cursor()

    def sql(self, sql):
        return self.cursor.execute(sql)

    def yml(self, yml):
        if Path.exists(yml):
            yml = Yml(yml).parameters
        for name, value in yml.items():
            self.sql(sql=value)
        self.cursor.close()
        self.db.close()
