from enum import Enum

class Type(Enum):
  google = 'google'
  facebook = 'facebook'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  

class Status(Enum):
  active = 'active'
  inactive = 'inactive'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  