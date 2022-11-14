

class GinaTrigger:
  """
  Class representing a Gina Trigger
  """

  def __init__(self, name, trigger_text):
    self.name = name
    self.trigger_text = trigger_text

  def get_text(self):
    return(self.trigger_text)

  def get_name(self):
    return(self.name)

  def get_all(self):
    return(dict{self.name: {
                            "trigger_name":
                            self.name,
                            "trigger_text":
                            self.trigger_text
                            }}
          )
