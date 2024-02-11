from dv import DV, Lexico, Token

#def DS(lexico):
#def CC(lexico):
  
def analise_sintatica(analise_lexica):
  lexico = Lexico(analise_lexica)
  x = lexico.next()
  if x.token == 'program':
    x = lexico.next()
    if x.classifier == 'IDENTIFIER':
      x = lexico.next()
      if x.token == ';':
        # nesse ponto, começam as analises para cada seçao
        print("ok")
        lexico = DV(lexico)
        lexico = DS(lexico)
        
      else:
        print('Erro sintático: esperado ";"')
    else:
      print('Erro sintático: esperado identificador do programa')
  else:
    print('Erro sintático: esperado "program"')

analise_lexica = []
with open('saida.txt', 'r') as file:
  linhas = file.readlines()
  for linha in linhas:
    linha = linha.strip()
    tokens = linha.split()
    novo_token = Token(tokens[0], tokens[1])
    analise_lexica.append(novo_token)

analise_sintatica(analise_lexica)
