from token_lexico import Lexico

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
        # cumpriu parte da lista de identificadores
        if x.token == ':':
          x = lexico.next()
          if x.token in ['integer', 'real', 'boolean']:
            x = lexico.next()
            if x.token == ';':
              # testa se tem mais declaracoes ou já é "program id"
              x = lexico.next()
            else:
              print('Erro sintático: esperado ";"')
          else:
            print('Erro sintático: esperado tipo')
        else:
          print('Erro sintático: esperado ":"')
      lexico.devolver()
      print('Declaração de variáveis concluída')
      return lexico 
    else:
      print('Erro sintático: esperado identificador')
  else:
    lexico.devolver()
    print('Declaração de variáveis concluída')
    return lexico 
