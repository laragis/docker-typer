from dataclasses import dataclass, field
from pathlib import Path
from environs import env


APP_ENV = env("APP_ENV", default="local")

DEFAULT_ENV_FILE = ".env"

@dataclass
class GlobalOptions:
  app_env: str = "local"
  env_file: str = DEFAULT_ENV_FILE
  working_dir: str = Path.cwd()
  dry_run: bool = False
  _dirty_fields: set = field(default_factory=set, init=False, repr=False)
  
  def __setattr__(self, key, value):
    if hasattr(self, key):
        current_value = getattr(self, key, None)
        if current_value != value:
            self._dirty_fields.add(key)
    super().__setattr__(key, value)

  def is_dirty(self, field: str) -> bool:
    return field in self._dirty_fields

  def get_dirty_fields(self) -> set:
    return self._dirty_fields

  def clear_dirty(self):
    self._dirty_fields.clear()
    

global_options = GlobalOptions()