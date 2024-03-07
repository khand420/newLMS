from enum import IntEnum
from enum import Enum

class Status(Enum):
  active = 'active'
  inactive = 'inactive'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]