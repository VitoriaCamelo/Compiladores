from token_lexico import Token, Lexico

''' 
lista_de_comandos -> comando l_d_c'
l_d_c' -> ; comando l_d_c' | e
comando -> id := expressao
  | ativacao_de_procedimento
  | comando_composto
  | if expressão then comando parte_else 
  |  while expressão do comando 
'''

def comando(lexico):
  x = lexico.next()
  if x.token == 'end':
    lexico = lexico.devolver()
    return lexico
  else:
    if x.classifier == 'IDENTIFIER':
      x = lexico.next()
      if x.token == ':=':
        print('analisar expressao')
      else:
        print('analisar lista de expressoes')
    elif x.token == 'begin':
        lexico = comando(lexico)
    elif x.token == 'if':
      print('analisar expressao')
      x = lexico.next()
      if x.token == 'then':
        lexico = comando(lexico)
        print('analisar parte-else')
      else:
        print('Erro sintático: esperado "then"')
    elif x.token == 'while':
      print('analisar expressao')
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
