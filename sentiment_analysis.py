 ###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Eduardo Santos de Moura
#            Rafael Rodrigues Ferreita Teles
#
# Email:    esm7@cin.ufpe.br
#            rrft@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Eduardo Santos de Moura, Rafael Rodrigues Ferreita Teles
#
###############################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = '''!"'`,;:.-?)\/([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result


def clean_stop_words(lista):
    '''Recebe como parametro uma lista e retorna a mesma limpa das stop words'''
    f = open("stopWords.txt")
    rawStopWords = f.readlines()
    f.close()
    stopWords = []
    for x in rawStopWords:
        stopWords.append(clean_up(x))
    final = []
    for x in lista:
        if x in stopWords:
            lista.remove(x)
    for x in lista:
        if x in stopWords:
            lista.remove(x)        
    for x in lista:
        if x in stopWords:
            lista.remove(x)
    for x in lista:
        if x in stopWords:
            lista.remove(x)
    for x in lista:
        if x in stopWords:
            lista.remove(x)
    return lista
    

def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return list(filter(lambda x: x != '',re.split('[{0}]'.format(separators),original)))
                    


def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    words = dict()
    f = open(fname, "r")
    listaFrases = f.readlines()
    f.close()
    listaPalavras = []
    listaPalavras2 = []  
    for frase in listaFrases:
        listaPalavras.append(split_on_separators(frase," "))
    for palavra in listaPalavras:
        listaAux = []
        for x in palavra:
            listaAux.append(clean_up(x))
        listaPalavras2.append(listaAux)    
    for x in listaPalavras2:
        clean_stop_words(x)
    for x in listaPalavras2:
        for y in x[1:]:
            escore = int(x[0])
            freq = 0
            if y in words:
                words[y] = ((int(words[y][0]) + escore) / 2),words[y][1]+1
            else:
                freq = freq + 1
                words[y] = escore,freq
            
    return words


def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	    retorna um vetor/lista de pares (escore,texto) dos
	    comentarios presentes no arquivo.
    '''    
    reviews = []
    f = open(fname, "r")
    listaFrases = f.readlines()
    f.close()
    listaPalavras = []
    listaPalavras2 = []
    listaFrases2 = []
    for frase in listaFrases:
        listaPalavras.append(split_on_separators(frase," "))
    for palavra in listaPalavras:
        listaAux = []
        for x in palavra:
            listaAux.append(clean_up(x))
        listaPalavras2.append(listaAux)    
    for x in listaPalavras2:
        clean_stop_words(x)
        listaFrases2.append(" ".join(x))
    for x in listaFrases2:
        reviews.append((int(x[0]),x[1:]))
           
    return reviews

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    for palavra in review:
      count = count+1
      if palavra in words:
      	score = score + words[palavra][0]
      else:
        score = score + 2
    
    return score/count


def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    listaErros = []
    j = 0
    for x in reviews:
      j = j + 1
      score = x[0]
      media = computeSentiment(x[1],words)
      if score > media:
        erro = score - media
      else:
        erro = media - score
      listaErros.append(erro)
    for x in listaErros:
      sse = sse + x * x
          
    return sse,sse/j

    
def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse[0]))
    print ('A media da soma do quadrado dos erros e\': {0}'.format(sse[1]))        

if __name__ == '__main__':
   main()
    
    
