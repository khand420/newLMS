from enum import IntEnum
from enum import Enum
class Type(Enum):
  mr = 'email'
  mrs = 'sms'
  ms = 'whatsapp'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class Smstype(Enum):
  english = 'english'
  hindi = 'hindi'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class Whatsapptype(Enum):
  text = 'text'
  media = 'media'
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
