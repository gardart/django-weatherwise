from .settings_default import *

try:
    from .local_settings import *  # type: ignore
except ImportError:
    pass
