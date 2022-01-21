import logging
import os
from pathlib import Path
from django.apps.config import AppConfig
from django.conf import settings
from django.views import debug

try:
    from livereloadish import watch_file
except ModuleNotFoundError:

    def watch_file(
        relative_path: str, absolute_path: str, requires_full_reload: bool
    ) -> bool:
        return requires_full_reload


try:
    old_builtin_template_path = debug.builtin_template_path
    old_current_dir = None
except AttributeError as e:
    old_builtin_template_path = None
    old_current_dir = debug.CURRENT_DIR


logger = logging.getLogger(__name__)
__all__ = ["TechnicalErrors"]


def new_builtin_template_path(name):
    new_path = Path(__file__).parent / "templates" / name
    if os.path.exists(new_path):
        watch_file(new_path.name, str(new_path), requires_full_reload=True)
        return new_path
    return old_builtin_template_path(name)


default_app_config = "technicalerrors.TechnicalErrors"


class TechnicalErrors(AppConfig):
    name = "technicalerrors"

    def ready(self) -> bool:
        return self.patch(settings.DEBUG)

    def patch(self, enabled: bool) -> bool:
        if enabled:
            if old_current_dir is not None:
                debug.CURRENT_DIR = Path(__file__).parent
                for file in (debug.CURRENT_DIR / "templates").iterdir():
                    if file.is_file():
                        watch_file(file.name, str(file), requires_full_reload=True)
                return True
            elif old_builtin_template_path is not None:
                debug.builtin_template_path = new_builtin_template_path
                return True
            return False
        return False
