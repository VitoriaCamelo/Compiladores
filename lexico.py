import sys
import string

def analisador_lexico(entrada):
  tupla_simples = tuple(string.ascii_letters)
  simbolos = string.ascii_letters + string.digits + "_"
  tupla_identificadores = tuple(simbolos)
  tupla_sem_r = tuple(simbolos.replace('r', ''))
  tupla_numeros = tuple(string.digits)
  
  palavras_reservadas = ['program', 'var', 'integer', 'real', 'boolean', 'procedure']
  palavras_reservadas += ['begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not']
  
  class Comentario:
    def __init__(self):
      self.pilha = []
      self.abriu = 0
    def abrir(self):
      self.abriu = 1
    def fechar(self):
      self.abriu = 0
    def estado(self):
      return self.abriu
      
  estados_finais = {
    'b': 'IDENTIFIER',
    'c': 'INTEGER'  ,
    'd': 'REAL',
    'e': 'DELIMITER',
    'ef': 'DELIMITER',
    'f': 'ATRIBUTION',
    'ag1': 'RELATION_OPERATORS',
    'ag2': 'RELATION_OPERATORS',
    'g': 'RELATION_OPERATOR',
    'h': 'ADITION_OPERATOR',
    'i': 'MULTIPLICATION_OPERATOR'
  }
  
  configuracoes = {
      'a': {
        (('{',), 'k'),
        (tupla_simples, 'b'),
        (tupla_numeros, 'c'),
        ((';', '.', ',', '(', ')',), 'e'),
        (':', 'ef'),
        (('='), 'g'),
        (('<'), 'ag1'),
        (('>'), 'ag2'),
        (('+', '-'), 'h'),
        #(('o'), 'ah'),
        (('*', '/'), 'i'),
        #(('a'), 'ai')
      },
      'b': {
        ((' '), 'a'),
        (tupla_identificadores, 'b'),
      },
      'c':{
        (tupla_numeros, 'c'),
        ('.', 'd')
      },
      'd': {
        (tupla_numeros, 'd'),
      },
      'k': {
        ('}', 'a'),
        (tupla_identificadores, 'k'),
      },
      'ef': {
        ('=', 'f'),
      },
      'e':{},
      'f': {},
      'g': {},
      'ag1': {
        (('=', '>'), 'g') 
      },
      'ag2': {
        (('=', '<'), 'g') 
      },
      'h': {},
      'ah': {
        ('r', 'h'),
        (tupla_sem_r, 'b')
      },
      'i': {}
  }
  
  estado_atual = 'a'
  string_atual = ''
  tabela = []
  linha = 0
  comentario = Comentario()
  for caractere in entrada:
    if not comentario.estado() and caractere == '{': 
      comentario.abrir()
    elif comentario.estado() and caractere == '}': 
      comentario.fechar()
    elif comentario.estado() == 0 and caractere == '}':
      print(f'Erro léxico: comentário não foi aberto antes da linha {linha+1}')
      sys.exit()
    elif not comentario.estado():
      if caractere == '\n': # and estado_atual in configuracoes
        # pode ter pegadinha aqui
        #print(string_atual, caractere, estado_atual)
        if estado_atual in estados_finais:
          tabela.append((string_atual, estados_finais[estado_atual], linha))
          string_atual = ''
        linha += 1
        estado_atual = 'a'
      elif caractere == ' ' and estado_atual in estados_finais:
        tabela.append((string_atual, estados_finais[estado_atual], linha))
        string_atual = ''
        estado_atual = 'a'
      elif caractere == ' ' and estado_atual == 'a':
        estado_atual = 'a'
      else:
        count = 0
        for opcoes in configuracoes[estado_atual]:
          if caractere in opcoes[0]:
            estado_atual = opcoes[1]
            count += 1
            if estado_atual != 'k' and caractere != '}':
              string_atual += caractere
    
        if count == 0:
          if estado_atual == 'k':
            estado_atual = 'k'
          else: 
            if estado_atual in estados_finais:
              tabela.append((string_atual, estados_finais[estado_atual], linha))
              string_atual = ''
            estado_atual = 'a'
            if caractere != ' ':
              string_atual = caractere
            for opcoes in configuracoes[estado_atual]:
              if caractere in opcoes[0]:
                estado_atual = opcoes[1]
                count += 1
            if count == 0:
              tabela.append((string_atual, 'ERROR', linha))
              string_atual = ''
  if estado_atual in estados_finais:
    tabela.append((string_atual, estados_finais[estado_atual], linha))
  else: 
    tabela.append((string_atual, 'ERROR', linha))
  
  #print("\n--- Aqui vem a tabela ---")
  if comentario.estado():
    print(f'Erro léxico: comentário não foi fechado na linha {linha+1}')
    sys.exit()
  with open('saida.txt', 'w') as f:
    more_lines = []
    for instancia in tabela:
        if instancia[0] in palavras_reservadas:
          more_lines.append("{:<16} {:^25} {:>12}".format(\
            instancia[0], 'RESERVED_WORD', instancia[2]+1))
        elif instancia[0] == 'and':
          more_lines.append("{:<16} {:^25} {:>12}".format(\
            instancia[0], 'MULTIPLICATION_OPERATOR', instancia[2]+1))
        elif instancia[0] == 'or':
          more_lines.append("{:<16} {:^25} {:>12}".format(\
            instancia[0], 'ADITION_OPERATOR', instancia[2]+1))
        else: 
          more_lines.append("{:<16} {:^25} {:>12}".format(\
            instancia[0], instancia[1], instancia[2]+1))
    f.write('\n'.join(more_lines))
      #print(f'{instancia[0]} \t {instancia[1]}\t {instancia[2]}')
