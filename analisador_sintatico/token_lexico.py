class Token:
  def __init__(self, token, classifier):
    self.token = token
    self.classifier = classifier

class Lexico:
  def __init__(self, analise_lexica):
    self.analise_lexica = analise_lexica
    self.conta_tokens = 0
  def next(self):
    self.conta_tokens += 1
    return self.analise_lexica[self.conta_tokens-1]
  def devolver(self):
    self.conta_tokens -=1
