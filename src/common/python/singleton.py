#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Singleton(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # 初回のみクラスを生成
        if not isinstance(cls._instance, cls):
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance

    @abstractmethod
    def initialize(self):
        pass
