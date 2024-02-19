import lexico

#############  Básico  ################
class Token:
  def __init__(self, token, classifier, linha):
    self.token = token
    self.classifier = classifier
    self.linha = linha

class Lexico:
  def __init__(self, analise_lexica):
    self.analise_lexica = analise_lexica
    self.conta_tokens = 0
  def next(self):
    self.conta_tokens += 1
    return self.analise_lexica[self.conta_tokens-1]
  def devolver(self):
    self.conta_tokens -=1
  def exibir(self):
    for token in self.analise_lexica[self.conta_tokens:]:
      print(token.token, token.classifier)

#############  Declaração de variáveis  ################
def DV(lexico):
  x = lexico.next()
  if x.token == 'var':
    ''' Verifica lista_declaracoes_variaveis 
    l_d_v -> l_d_i : tipo ; l_d_v'
    l_d_v' -> l_d_i : tipo ; l_d_v' | e
    ''' 
    x = lexico.next()
    ''' Precisa ter id
    l_d_i -> id l_d_i'
    l_d_i' -> , id l_d_i' | e
    '''
    if x.classifier == 'IDENTIFIER':
      while(x.classifier == 'IDENTIFIER'):
        x = lexico.next()
        # loop (, id)
        while(x.token == ','):
          x = lexico.next()
          if x.classifier == 'IDENTIFIER':
            x = lexico.next()
          else:
            print('Erro sintático: esperado identificador')
            return 'erro'
        # cumpriu parte da lista de identificadores
        if x.token == ':':
          x = lexico.next()
          if x.token in ['integer', 'real', 'bool']:
            x = lexico.next()
            if x.token == ';':
              # testa se tem mais declaracoes ou já é "program id"
              x = lexico.next()
            else:
              print('Erro sintático: esperado ";"')
              return 'erro'
          else:
            print('Erro sintático: esperado tipo')
            return 'erro'
        else:
          print('Erro sintático: esperado ":"')
          return 'erro'
      lexico.devolver()
      print('Declaração de variáveis concluída')
      return lexico 
    else:
      print('Erro sintático: esperado identificador')
      return 'erro'
  else:
    lexico.devolver()
    print('Declaração de variáveis concluída')
    return lexico

#############  Declaração de subprogramas  ################
def DS(lexico):
  ''' Como funciona
  d_d_subs -> d_d_s ; d_d_subs' | e
  d_d_s -> 
  procedure id argumentos;
  declarações_variáveis
  declarações_de_subprogramas
  comando_composto
  '''
  x = lexico.next() # possivel programa para programa sem primeiro passo
  if x.token == 'procedure':
    while(x.token == 'procedure'):
      x = lexico.next()
      if x.token == 'id':
        lexico = DV(lexico)
        x = lexico.next()
        if x.token == ';':
          lexico = DV(lexico)
          x = lexico.next()
        else:
          print('Erro sintático: esperado ";"')
          return 'erro'
      else:
        print('Erro sintático: esperado "id"')
        return 'erro'
    lexico.devolver()
    print('Declaração de subprogramas concluída')
    return lexico
  else:
    lexico.devolver()
    print('Declaração de subprogramas concluída')
    return lexico

#############  Construção do léxico  ################
def analise_sintatica(analise_lexica):
  lexico = Lexico(analise_lexica)
  x = lexico.next()
  if x.token == 'program':
    x = lexico.next()
    if x.classifier == 'IDENTIFIER':
      x = lexico.next()
      if x.token == ';':
        print("Um programa foi declarado")
        resposta = DV(lexico)
        if resposta == 'erro':
          lexico.exibir()
          print('Análise finalizada')
        else:
          resposta = DS(resposta)
          if resposta == 'erro':
            lexico.exibir()
            print('Análise finalizada')
      else:
        print('Erro sintático: esperado ";"')
        return 'erro'
    else:
      print('Erro sintático: esperado identificador do programa')
      return 'erro'
  else:
    print('Erro sintático: esperado "program"')
    return 'erro'

#############  Fluxo léxico (testes)  ################
with open('entrada.pas', 'r') as arquivo:
  entrada = arquivo.read()
  #print(entrada)
  lexico.analisador_lexico(entrada)
  

#############  Fluxo principal  ################
analise_lexica = []
with open('saida.txt', 'r') as file:
  linhas = file.readlines()
  for linha in linhas:
    linha = linha.strip()
    tokens = linha.split()
    novo_token = Token(tokens[0], tokens[1], tokens[2])
    analise_lexica.append(novo_token)

analise_sintatica(analise_lexica)
