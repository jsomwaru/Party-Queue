import importlib.util
import os
import sys
from enum import Enum


class AppConfig:
    @staticmethod
    def redis_uri():
        return os.environ.get("REDIS_URI", "redis://127.0.0.1:6379")

    @staticmethod    
    def get_device_backend():
        backend = None
        if sys.platform == "darwin":
            backend = _lazy_import("partyq.bluetooth.io_bluetooth")
        elif sys.platform == "linux":
            backend = _lazy_import("partyq.bluetooth.lbm")
        return backend
    
    @property
    @staticmethod
    def PLATFORM():
        return sys.platform

class Cookies(Enum):
    AUTH = "authenticated"

def _lazy_import(name: str):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module
