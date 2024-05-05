import sys
import importlib.util

AUTH = "authenticated"
PLATFORM = sys.platform

def _lazy_import(name: str):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def get_device_backend():
    backend = None
    if sys.platform == "darwin":
        backend = _lazy_import("partyq.bluetooth.io_bluetooth")
    elif sys.platform == "linux":
        backend = _lazy_import("partyq.bluetooth.linux")
    return backend

