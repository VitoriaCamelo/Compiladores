from token_lexico import Lexico
from dv import DV
from cc import CC

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
      else:
        print('Erro sintático: esperado "id"')
    lexico.devolver()
    lexico = CC(lexico)
    # repensar mensagem
  else:
    lexico.devolver()
    print('Declaração de subprogramas concluída')
    return lexico
