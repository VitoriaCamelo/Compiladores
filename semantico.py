import sys
import lexico

# ADEQUAR AO WHILE, AO IF E À PASSAGEM DE PARÂMETROS (FUNÇÕES)

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
    return self
  def exibir(self):
    for token in self.analise_lexica[self.conta_tokens:]:
      print(token.token, token.classifier, token.linha)

#############  Apoio do semântico  ################
class PIdentificadores:
  def __init__(self):
    self.pilha = []
    self.num_begin = 0
  def marcar(self):
    self.pilha.append(['$', 'marcador'])
  def topo(self):
    return self.pilha[-1]
  def topo_indice(self):
    return len(self.pilha)-1
  def empilhar(self, token, tipo): # entrada
    self.pilha.append([token, tipo])
  def desempilhar(self): # saida
    simbolo = self.topo()[0]
    while(simbolo!='$'):
      self.pilha.pop()
      simbolo = self.topo()[0]
    self.pilha.pop()
  def declaracao(self, token): # verificar se pode declarar
    simbolo = self.topo()[0]
    indice = self.topo_indice()
    while(simbolo!='$'):
      if simbolo == token:
        return False
      else:
        indice -= 1
        simbolo = self.pilha[indice][0]
    return True
  def procura(self, token): # verificar para uso
    if self.topo_indice() != -1:
      indice = self.topo_indice()
      simbolo = self.pilha[indice][0]
      while(indice != -1):
        if simbolo == token:
          return True
        else:
          indice -= 1
          simbolo = self.pilha[indice][0]
      return False
    return False
  def begin(self):
    self.num_begin += 1
  def end(self):
    self.num_begin -= 1
  def verifica_begin(self):
    return self.num_begin > 0
  def exibir(self):
    for token, tipo in self.pilha:
      print(token, tipo)
  def tipificar(self, tipo):
    tipo_atribuido = self.topo()[1]
    indice = self.topo_indice()
    while tipo_atribuido is False:
      self.pilha[indice][1] = tipo
      indice = indice-1
      tipo_atribuido = self.pilha[indice][1]
  def tipo_simbolo(self, token):
    if self.topo_indice() != -1:
      indice = self.topo_indice()
      simbolo = self.pilha[indice][0]
      while(indice != -1):
        if simbolo == token:
          return self.pilha[indice][1]
        else:
          indice -= 1
          simbolo = self.pilha[indice][0]

class PCT:
  def __init__(self):
    self.pilha = []
  def marcar(self):
    self.pilha.append('$')
  def empilhar(self, tipo): # novo tipo
    self.pilha.append(tipo)
  def desempilhar(self):
    while self.topo_indice() != -1:
      self.pilha.pop()
  def topo(self):
    return self.pilha[-1]
  def subtopo(self):
    return self.pilha[-2]
  def atualizar(self, novo_tipo):
    self.pilha.pop()
    self.pilha.pop()
    self.empilhar(novo_tipo)
  def exibir(self):
    for tipo in self.pilha:
      print(tipo)
  def tamanho(self):
    return len(self.pilha)
  def verificacao_simples(self):
    return self.topo() == pid.tipo_simbolo(self.subtopo())
  def topo_indice(self):
    return len(self.pilha)-1
  def verificacao(self):
    while self.topo_indice() > 2: # antes era 1
      tipo_topo = self.topo()
      tipo_subtopo = self.subtopo()
      self.pilha.pop()
      self.pilha.pop()
      if tipo_topo == 'integer' and tipo_subtopo == 'integer':
        self.empilhar('integer')
      elif tipo_topo in ['real', 'integer'] and tipo_subtopo in ['real', 'integer']:
        self.empilhar('real')
      else:
        print(f'Tipos/operação incompatível(is) {tipo_topo} e {tipo_subtopo}')
        sys.exit()
    return self.verificacao_simples()
  def avaliar(self):
    if (pct.tamanho() == 3 and not pct.verificacao_simples()) or \
    (pct.tamanho() > 3 and not pct.verificacao()):
      pct.exibir()
      print(pct.topo(), pct.subtopo(), pid.tipo_simbolo(pct.subtopo()))
      print(f'Erro semântico: {pct.subtopo()} recebeu {pct.topo()}')
      sys.exit()
    '''
    elif pct.tamanho() >= 3:
    print(pct.topo(), pct.subtopo(), pct.topo())
    '''

pid = PIdentificadores()
pct = PCT()
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
        if pid.declaracao(x.token):
          pid.empilhar(x.token, False)
        else:
          print(f'Erro semântico: {x.token} já declarado antes da linha {x.linha}')
          sys.exit()
        x = lexico.next()
        # loop (, id)
        while(x.token == ','):
          x = lexico.next()
          if x.classifier == 'IDENTIFIER':
            if pid.declaracao(x.token):
              pid.empilhar(x.token, False)
            else:
              print(f'Erro semântico: {x.token} já declarado antes da linha {x.linha}')
              sys.exit()
            x = lexico.next()
          else:
            print('Erro sintático: esperado identificador na linha ', x.linha)
            sys.exit()
        # cumpriu parte da lista de identificadores
        if x.token == ':':
          x = lexico.next()
          if x.token in ['integer', 'real', 'boolean']:# já foi bool
            pid.tipificar(x.token)
            x = lexico.next()
            if x.token == ';':
              # testa se tem mais declaracoes ou já é "program id"
              x = lexico.next()
            else:
              print('Erro sintático: esperado ";" na linha ', x.linha)
              sys.exit()
          else:
            lexico = lexico.devolver()
            print('Erro sintático: esperado tipo na linha ', x.linha)
            sys.exit()
        elif x.classifier == 'IDENTIFIER': # esqueceu , - existem mais casos?
          lexico = lexico.devolver()
          print('Erro sintático: esperado "," na linha ', x.linha)
          sys.exit()
        else:
          lexico = lexico.devolver()
          print('Erro sintático: esperado ":" na linha ', x.linha)
          sys.exit()
      lexico.devolver()
      print('Declaração de variáveis concluída na linha ', x.linha)
      return lexico 
    else:
      print('Erro sintático: esperado identificador na linha ', x.linha)
      sys.exit()
  else:
    lexico.devolver()
    print('Declaração de variáveis concluída na linha ', x.linha)
    return lexico

#############  Declaração de subprogramas  ################
def lista_parametros(lexico): # base = A:integer, B:real
  '''
  lista_de_parametros →
  lista_de_identificadores: tipo l_p'
  l_p' -> , lista_de_identificadores: tipo
  '''
  x = lexico.next()
  if x.classifier == 'IDENTIFIER': # else
    if pid.declaracao(x.token):
      pid.empilhar(x.token, False)
    else:
      print(f'Erro semântico: {x.token} já declarado antes da linha {x.linha}')
      sys.exit()
    x = lexico.next()
    if x.token == ':':
      x = lexico.next()
      if x.token in ['integer', 'real', 'bool']:
        x = lexico.next()
        if x.token == ',':
          lexico = lista_parametros(lexico)
          return lexico
        else:
          lexico = lexico.devolver()
          print('Declaração de parâmetros concluída na linha ', x.linha)
          return lexico
      else:
        print('Erro sintático: esperado tipo na linha ', x.linha)
        sys.exit()
    else:
      print('Erro sintático: esperado ":" na linha ', x.linha)
      sys.exit()

def DS(lexico):
  count_abriu = 0
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
      if x.classifier == 'IDENTIFIER': # id é id ou identifier?
        if pid.declaracao(x.token):
          pid.empilhar(x.token, 'programa')
          pid.marcar()
        else:
          print(f'Erro semântico: {x.token} já declarado antes da linha {x.linha}')
          sys.exit()
        x = lexico.next()
        if x.token == '(':
          count_abriu = 1
          lexico = lista_parametros(lexico) 
          #if lexico == 'erro':
          #  print('erro')
          #  return erro
          #else:
          x = lexico.next()
          if x.token != ')':
            print('Erro sintático: esperado ")" na linha', x.linha)
            sys.exit()
        if count_abriu == 1: # NAO TINHA
          x = lexico.next()
        if x.token != ';':
          #print(x.token, x.classifier, x.linha)
          print('Erro sintático: esperando ";" na linha', x.linha)
          sys.exit()
        lexico = DV(lexico) # ok
        lexico = CC(lexico) # NAO TINHA, TIRAR SER DER PROBLEMA
        x = lexico.next()
      else:
        print('Erro sintático: esperado "id" na linha', x.linha)
        sys.exit()
    ##
    lexico = lexico.devolver()
    #lexico = CC(lexico) # TINHA ANTES: DEVOLVER COM CAUTELA
    #if lexico == 'erro':
    #  return 'erro'
    print('Declaração de subprogramas concluída na linha', x.linha)
    return lexico
  else:
    lexico.devolver()
    print('Declaração de subprogramas concluída', x.linha)
    return lexico

#############  Comando composto  ################
def termo1(lexico):
  # termo' -> op_multiplicativo fator termo' | e
  x = lexico.next()
  if x.token in ['*', '/', 'and']: 
    lexico = fator(lexico)
    lexico = termo1(lexico)
    return lexico
  else:
    lexico = lexico.devolver()
    return lexico

def fator(lexico):
  ''' Como termo funciona:
  fator →
  id
  | id(lista_de_expressões)
  | num_int
  | num_real
  | true
  | false
  | (expressão)
  | not fator 
  '''
  x = lexico.next()
  # num_int -> INTEGER, num_real -> REAL
  if x.token in ['true', 'false']:
    pct.empilhar('boolean')
    return lexico
  elif x.classifier in ['INTEGER', 'REAL']: 
    pct.empilhar(x.classifier.lower())
    return lexico
  elif x.token == '(':
    lexico = expressao(lexico)
    x = lexico.next()
    if x.token == ')':
      return lexico
    else:
      print('Erro sintático: esperado ")" na linha ', x.linha)
      sys.exit()
  elif x.classifier == 'IDENTIFIER': # id ou identifier?
    if not pid.procura(x.token):
      print(f'Erro semântico: "{x.token}" (linha {x.linha}) não foi declarado')
      sys.exit()
    pct.empilhar(pid.tipo_simbolo(x.token))
    x = lexico.next()
    if x.token == '(':
      lexico = lista_expressoes(lexico)
      x = lexico.next()
      if x.token == ')':
        return lexico
    else:
      lexico.devolver()
      return lexico
  elif x.token == 'not':
    lexico = fator(lexico)
    return lexico
  else:
    print('Erro sintático: esperado termo na linha ', x.linha)
    sys.exit()

def e_s(lexico):
  '''
  e_s' -> (+ | - | or) (fator termo') e_s' | e
  '''
  x = lexico.next()
  if x.token in ['+', '-', 'or']:
    lexico = fator(lexico)
    lexico = termo1(lexico)
    lexico = e_s(lexico)
    return lexico
  else:
    lexico = lexico.devolver()
    return lexico

def expressao_simples(lexico):
  conta_operador = 0
  '''
  expressao_simples -> (fator termo') e_s' 
    | (+ | -) (fator termo') e_s'
  '''
  x = lexico.next()
  if x.token in ['+', '-']:
    conta_operador += 1
    lexico = fator(lexico)
    lexico = termo1(lexico)
    lexico = e_s(lexico)
    return lexico
  else:
    lexico = lexico.devolver()
    lexico = fator(lexico) 
    lexico = termo1(lexico)
    lexico = e_s(lexico)
    return lexico

def expressao(lexico):
  '''
  expressao -> expressão_simples
  | expressão_simples op_relacional expressão_simples
  op_relacional -> = | < | > | <= | >= | <>
  '''
  lexico = expressao_simples(lexico)
  x = lexico.next()
  if x.token in ['=', '<', '>', '<=', '>=', '<>']:
    lexico = expressao_simples(lexico)
    return lexico
  else:
    lexico = lexico.devolver()
    return lexico

def lista_expressoes(lexico):
  lexico = expressao(lexico)
  x = lexico.next()
  if x.token == ',': # está certo?
    while x.token == ',':
      lexico = expressao(lexico)
      x = lexico.next()
    return lexico
  else:
    lexico = lexico.devolver()
    return lexico

def comando(lexico):
  '''
  lista_de_comandos -> comando l_d_c'
  l_d_c' -> ; comando l_d_c' | e
  comando -> id := expressao 
    | ativacao_de_procedimento 
    | comando_composto 
    | if expressão then comando (parte_else → else comando | ε) 
    |  while expressão do comando 
  '''
  x = lexico.next()
  if x.token == 'end':
    lexico = lexico.devolver()
    return lexico, 0
  else:
    if x.classifier == 'IDENTIFIER':
      #pid.exibir()
      if not pid.procura(x.token):
        print(f'Erro semântico: "{x.token}" (linha {x.linha}) não foi declarado')
        sys.exit()
      pct.empilhar(x.token)
      x = lexico.next()
      if x.token == ':=':
        lexico = expressao(lexico)
        return lexico, 0
      else:
        lexico = lexico.devolver() # NAO TINHA ANTES, SE DER ERRADO, TIRAR
        x = lexico.next()
        if x.token == '(':
          lexico = lista_expressoes(lexico)
          x = lexico.next()
          if x.token == ')':
            return lexico, 0
          else:
            print('Erro sintático: esperado ")" na linha ', x.linha)
            sys.exit()
        else:
          lexico = lexico.devolver()
          return lexico, 0
    elif x.token == 'begin':
        lexico = lista_comandos(lexico)
        x = lexico.next()
        if x.token == 'end':
          #lexico = lexico.devolver() # NAO TINHA ANTES, TIRAR SE PROVOCAR ERRO
          return lexico, 0
        else:
          print('Erro sintático: esperado "end" na linha ', x.linha)
          sys.exit()
    elif x.token == 'if': # precisa resultar em booleano
      pct.marcar()
      lexico = expressao(lexico)
      x = lexico.next()
      pct.desempilhar()
      if x.token == 'then':
        pct.marcar()
        lexico, avaliado = comando(lexico)
        pct.avaliar()
        pct.desempilhar()
        x = lexico.next()
        if x.token == 'else':
          pct.marcar()
          lexico, avaliado = comando(lexico)
          pct.avaliar()
          pct.desempilhar()
          return lexico, 1
        else:
          lexico = lexico.devolver()
          return lexico, 1
      else:
        print('Erro sintático: esperado "then" na linha ', x.linha)
        sys.exit()
    elif x.token == 'while': # precisa resultar em booleano
      pct.marcar()
      lexico = expressao(lexico)
      pct.desempilhar()
      x = lexico.next()
      if x.token == 'do':
        pct.marcar()
        lexico, avaliado = comando(lexico)
        pct.avaliar()
        pct.desempilhar()
        return lexico, 1
      else:
        print('Erro sintático: esperado "do" na linha ', x.linha)
        sys.exit()

def lista_comandos(lexico):
  lexico, avaliado = comando(lexico)
  if not avaliado: 
    pct.avaliar()
  pct.desempilhar()
  x = lexico.next()
  if x.token == ';':
    while x.token == ';':
      pct.marcar()
      lexico, avaliado = comando(lexico)
      if not avaliado:
        pct.avaliar()
      pct.desempilhar()
      x = lexico.next()
    lexico = lexico.devolver() # ESTAVA DANDO ERRO ANTES
    return lexico
  else:
    lexico = lexico.devolver()
    return lexico

def CC(lexico):
  x = lexico.next()
  if x.token == 'begin':
    # pode ter ou não comandos
    pid.begin()
    pct.marcar()
    lexico = lista_comandos(lexico)
    x = lexico.next()
    if x.token == 'end':
      #print('Devolvendo na linha', x.linha)
      pid.desempilhar()
      pct.desempilhar()
      return lexico
    else:
      print('Erro sintático: esperado "end" na linha', x.linha)
      sys.exit()
  else:
    print('Erro sintático: esperado "begin" na linha', x.linha)
    sys.exit()

#############  Construção do léxico  ################ 
def analise_sintatica(analise_lexica):
  lexico = Lexico(analise_lexica)
  x = lexico.next()
  if x.token == 'program':
    pid.marcar()
    x = lexico.next()
    if x.classifier == 'IDENTIFIER':
      pid.empilhar(x.token, 'programa')
      x = lexico.next()
      if x.token == ';':
        print("Um programa foi declarado")
        resposta = DV(lexico)
        #if resposta == 'erro':
        #  lexico.exibir()
        #  print('Análise finalizada')
        #else:
        resposta = DS(resposta)
          #if resposta == 'erro':
          #  lexico.exibir()
          #  print('Análise finalizada')
          #else:
        resposta = CC(resposta)
          #  if resposta == 'erro':
          #    print('Análise finalizada')
          #  else:
          #    print('\n FINALIZANDO \n')
        try:
          x = lexico.next()
          if x.token == '.':
            print('Programa está sintaticamente correto')
          else:
            print('Erro sintático: esperado "." na linha', x.linha)
            print('Recebido: ', x.token)
            resposta.exibir()
            sys.exit()
        except Exception as e:
          print('Erro sintático: esperado "."')
      else:
        print('Erro sintático: esperado ";" na linha', x.linha)
        sys.exit()
    else:
      print('Erro sintático: esperado identificador do programa na linha', x.linha)
      sys.exit()
  else:
    print('Erro sintático: esperado "program" na linha', x.linha)
    sys.exit()

#############  Fluxo léxico (testes)  ################

with open('SemanticoTest.pas', 'r') as arquivo:
  entrada = arquivo.read()
  #print(entrada)
  lexico.analisador_lexico(entrada)



#############  Fluxo principal  ################
analise_lexica = []
with open('saida.txt', 'r') as file:
  linhas = file.readlines()
  for linha in linhas:
    tokens = linha.split()
    novo_token = Token(tokens[0], tokens[1], tokens[2])
    analise_lexica.append(novo_token)

analise_sintatica(analise_lexica)
