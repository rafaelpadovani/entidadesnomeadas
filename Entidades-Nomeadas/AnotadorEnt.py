import nltk
import codecs
import sys
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np

TotalPessoas = 0
TotalLocais = 0
TotalOrganizacoes = 0

Names = []

Locais = []

Organizacoes = []

with codecs.open ('nomesbr.txt','r', 'utf-8') as f :
    Names = [name.rstrip() for name in f]

with codecs.open ('locais.txt','r', 'utf-8') as f2 :
    Locais = [local.rstrip() for local in f2]

with codecs.open ('organizacoes.txt','r', 'utf-8') as f3 :
    Organizacoes = [organizacao.rstrip() for organizacao in f3]

preposicoes = ['da','do','das','dos','na','nas','no','nos','de','pela','à', 'a', 'ante', 'após', 'até', 'com', 'contra', 'de', 'desde', 'em', 'entre', 'para', 'perante', 'por', 'sem', 'sob', 'sobre', 'trás']


if __name__ == '__main__':
    isfile = False
    if len(sys.argv) < 2:
        print ("Usage:", sys.argv[0]," arq.txt|name")
        sys.exit(1)

    argument = sys.argv[1]
    if '.txt' in argument:
       isfile = True

text = codecs.open(argument, 'r', 'utf-8')

text2 = codecs.open('/Users/.../Entidades-Nomeadas/anotados/'+argument, 'w', 'utf-8')


empresa = False
compo = []


def nextwords(target, source, rule):
    listanome = []
    listanome.append(target)
    prox = source.index(target)+1
    global empresa
    #print('prox')
    #print(prox)
    #palavra = source[prox]
    while prox < len(source):
        palavra = source[prox]
        if (palavra == 'S.A.') or (palavra == 'S/A') or (palavra == 'Ltda') or (palavra == 'LTDA') or (palavra == 's.a.') or (palavra == 's/a'):
            listanome.append(source[prox])
            empresa = True
            break
        if (palavra == 'do') or (palavra == 'de') or (palavra == 'da') or (palavra == 'dos') or (palavra == 'das') or (palavra == 'em'):
            proxprep = source[prox+1]
            if proxprep[0].isupper():
                listanome.append(source[prox])
                listanome.append(source[prox+1])
                prox = prox + 1
        
        
        #if source[prox] in rule:
        elif palavra[0].isupper():
            listanome.append(source[prox])
        elif (palavra[0].islower()) or (palavra == ',') or (palavra == '.') or (palavra == '–') or (palavra == '-') or (palavra == ':') or (palavra == '(') or (palavra == ')'):
            break
        prox = prox + 1

    return listanome
    
        

lista = []


nomes = []
scape = 1

for item in text:
    lista = word_tokenize(item)
    
    for word in lista:
        nomes = []
        locais = []
        organizacoes = []
        print(word)
        if scape != 1:
            scape = scape-1
            continue
        if word in Names:
            if word not in nomes:
                nomes = nextwords(word, lista, Names)
                #print('array nomes')
                #print(nomes)
                nomesstr = ' '.join(nomes)
                if empresa:
                    text2.write('<ORGANIZACAO>' + nomesstr + '</ORGANIZACAO> ')
                    empresa = False
                    TotalOrganizacoes = TotalOrganizacoes + 1
                else:
                    text2.write('<PESSOA>' + nomesstr + '</PESSOA> ')
                    TotalPessoas = TotalPessoas + 1
                #text2.write('<PESSOA>' + str(nomes) + '</PESSOA> ')
                #print('tamanho nomes')
                scape = len(nomes)
                #print(scape)
        elif word in Locais:
            if word not in locais:
                locais = nextwords(word, lista, Locais)
                locaisstr = ' '.join(locais)
                if empresa:
                    text2.write('<ORGANIZACAO>' + locaisstr + '</ORGANIZACAO> ')
                    empresa = False
                    TotalOrganizacoes = TotalOrganizacoes + 1
                else:
                    text2.write('<LUGAR>' + locaisstr + '</LUGAR> ')
                    TotalLocais = TotalLocais + 1
                #text2.write('<LUGAR>' + str(locais) + '</LUGAR> ')
                #print('tamanho locais')
                scape = len(locais)
                #print(scape)
        elif word in Organizacoes:
            if word not in organizacoes:
                organizacoes = nextwords(word, lista, Organizacoes)
                organizacoesstr = ' '.join(organizacoes)
                text2.write('<ORGANIZACAO>' + organizacoesstr + '</ORGANIZACAO> ')
                TotalOrganizacoes = TotalOrganizacoes + 1
                #text2.write('<ORGANIZACAO>' + str(organizacoes) + '</ORGANIZACAO> ')
                #print('tamanho organizazacoes')
                scape = len(organizacoes)
                #print(scape)
        else:
            text2.write(word+' ')


print('PESSOAS: ', TotalPessoas)
print('LUGAR: ', TotalLocais)
print('ORGANIZACOES: ', TotalOrganizacoes)


    

        


