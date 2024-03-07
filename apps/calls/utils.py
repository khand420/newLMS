from enum import IntEnum
from enum import Enum

class Status(Enum):
  active = '1'
  inactive = '0'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]