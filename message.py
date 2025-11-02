from user import User

class Message:
  def __init__ (self, uFrom: User, uTo: User, msg: str = "", key: str = ""):
    self.uFrom = uFrom
    self.uTo = uTo
    self.msg = msg
    self.key = key
