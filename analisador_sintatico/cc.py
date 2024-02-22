
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
  if x.token in ['num_int', 'num_real', 'true', 'false']:
    return lexico
  elif x.token == '(':
    lexico = expressao(lexico)
    x = lexico.next()
    if x.token == ')':
      return lexico
    else:
      print('Erro sintático: esperado ")" na linha ', x.linha)
  elif x.token == 'id':
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
  else:
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
    lexico.devolver()
    return lexico
    
def comando(lexico):
  '''
  lista_de_comandos -> comando l_d_c'
  l_d_c' -> ; comando l_d_c' | e
  comando -> id := expressao
    | ativacao_de_procedimento
    | comando_composto
    | if expressão then comando parte_else 
    |  while expressão do comando 
  '''
  x = lexico.next()
  if x.token == 'end':
    lexico.devolver()
    return lexico
  else:
    if x.classifier == 'IDENTIFIER':
      x = lexico.next()
      if x.token == ':=':
        lexico = expressao(lexico)
        return lexico
      else:
        print('analisar lista de expressoes')
    elif x.token == 'begin':
        lexico = comando(lexico)
    elif x.token == 'if':
      lexico = expressao(lexico)
      x = lexico.next()
      if x.token == 'then':
        lexico = comando(lexico)
        print('analisar parte-else')
      else:
        print('Erro sintático: esperado "then"')
    elif x.token == 'while':
      lexico = expressao(lexico)
      x = lexico.next()
      if x.token == 'do':
        lexico = comando(lexico)
      else:
        print('Erro sintático: esperado "do"')
    

    
def CC(lexico):
  x = lexico.next()
  if x.token == 'begin':
    # pode ter ou não comandos
    lexico = comando(lexico)
    x = lexico.next()
    if x.token == 'end':
      return lexico
    else:
      print('Erro sintático: esperado "end"')
  else:
    print('Erro sintático: esperado "begin"')
