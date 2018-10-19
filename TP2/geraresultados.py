import math
import csv
import os,sys


def lerOriginais(arq):
    with open(arq) as f:
        lst = []
        r = csv.DictReader(f)
        for x in r:
            lst.append(x['Cortes'])
    return lst


def buscaNoOriginal(id,arq):
    return lst[id]


def lerDeArquivoOriginal(nomeDoArquivo):
    lst=[]
    with open(nomeDoArquivo) as arq:
        conteudoDoArq= arq.read().split("-")
        for x in range(len(conteudoDoArq)):
            lst += [conteudoDoArq[x]]
    return lst


def lerDeArquivoGerado(nomeDoArquivo):
    lst=[]
    with open(nomeDoArquivo) as arq:
        conteudoDoArq= arq.read().split(",")
        for x in range(len(conteudoDoArq)):
            lst += [conteudoDoArq[x]]
    return lst


def humanTimeToMSECOriginal(tempoHumano):
    lst=[]
    for x in range(len(tempoHumano)):
        #tempoHumano = str(tempoHumano)
        if(tempoHumano[x]=='nao muda' or tempoHumano[x]=='não muda'):
            break;
        elif(tempoHumano[x]==''):
            break;
        else:
            str_aux = tempoHumano[x].split(":")
            minuto = int(str_aux[0])*6000
            if(str_aux[-1]==''):
                break;
            segundo =int(str_aux[-1])*1000
            lst.append( minuto+ segundo)
    return lst


def humanTimeToMSECGerado(tempoHumano):
    lst=[]
    for x in range(len(tempoHumano)):
        lst.append((tempoHumano[x]))
    return lst


def compara(lista, valor,limiar):
    for x in range(len(lista)):
        if( abs( valor-lista[x])<= limiar):
            return 1
    return 0


def listaMaior(l1,l2,limiar):
    totalEncontrado=0
    if(len(l1)>=len(l2)):
        for x in range(len(l2)):
            if(compara(l1,l2[x],limiar)):
                totalEncontrado=totalEncontrado	+1
    else:
        for x in range(len(l1)):
            if(compara(l2,l1[x],limiar)):
                totalEncontrado=totalEncontrado	+1
    return totalEncontrado

def main():
    #print("---METRICAS---\n")
    #nomeArqOriginal= input("Digite o Nome do arquivo Original: ")
    lerOriginais('Cortes  - Base.csv')
    limiar = float(input("limiar msec: "))
    #print("limiar msec: "+ str(limiar))
    nomeArqOriginal=input("Coletado")

    original = lerDeArquivoOriginal(nomeArqOriginal)
    originalTemposEmMSEC = humanTimeToMSECOriginal(original)
    #nomeArqGerado = input("Digite o nome do arquivo que foi gerado pelo algoritmo: ")
    nomeArqGerado = input()
    gerado = lerDeArquivoGerado(nomeArqGerado)
    geradoTemposEmMSEC= humanTimeToMSECGerado(gerado)
    acertos= listaMaior(originalTemposEmMSEC,geradoTemposEmMSEC,limiar)
    quantidadeAlgoritmoGerado= len(geradoTemposEmMSEC)
    quantidadeOriginal=  len(originalTemposEmMSEC)
    precisao= (acertos/quantidadeAlgoritmoGerado)
    print("Quantidade de Cenas Detectada pelo algoritmo: "+str(quantidadeAlgoritmoGerado) )
    print("Quantidade de Cenas Detectadas manualmente: "+str(quantidadeOriginal) )

    print("Precisao: "+ str(100.0*precisao)+" %" )
    revocacao = (acertos/ quantidadeOriginal)
    print("Revocação: "+ str(100.0*revocacao)+ " %")

#main()

def todosOsResulados():
    originais = lerOriginais('/home/katiely/Vídeos/Take/CSV/Cortes  - Base.csv')
    lst=[]
    with open('hist_300.txt') as arq:
        conteudoDoArq= arq.read().split("\n")
    a=[]
    for i in range(len(originais)):
        a.append((originais[i].split('-')))
    h=0

    for x in range(0,len(conteudoDoArq)):

        if(a[x]=="nao muda"):
            print('huehue')
        else:
            if(conteudoDoArq[x]==''):
                print(str(x+1)+'-->Precisao 00')
            #print("")
            else:
                limiar = 1011
                lista_g = conteudoDoArq[x].split(',')
                geradoTemposEmMSEC =  humanTimeToMSECGerado(lista_g)
                #print(geradoTemposEmMSEC)
                #geradoTemposEmMSEC = [ float(x*1000 for x in geradoTemposEmMSEC]
                originalTemposEmMSEC= humanTimeToMSECOriginal(a[x])
                #print(originalTemposEmMSEC)
                l= [float(x)*1000 for x in geradoTemposEmMSEC]
                acertos= listaMaior((originalTemposEmMSEC),(l),limiar)
                quantidadeAlgoritmoGerado= len(geradoTemposEmMSEC)+1
                quantidadeOriginal=  len(originalTemposEmMSEC)+1
                precisao= float(acertos/quantidadeAlgoritmoGerado)
                #print(len(quantidadeOriginal))
                #print(str(x+1)+"\nQuantidade de Cenas Detectada pelo algoritmo: "+str(quantidadeAlgoritmoGerado) )
                #print("Quantidade de Cenas Detectadas manualmente: "+str(quantidadeOriginal) )
                print(str(x+1)+"\nPrecisao: "+ str(100.0*precisao)+" % " )
                revocacao = (acertos/ quantidadeOriginal)
                print("Revocação: "+ str(100.0*revocacao)+ " %")
                print(str(x+1)+" algoritmo: "+str(quantidadeAlgoritmoGerado)+ "  MAN: "+  str(quantidadeOriginal))
todosOsResulados()

def mostraQuantidadeCortes():
    s=0
    originais = lerOriginais('/home/katiely/Vídeos/Take/CSV/Cortes  - Base.csv')
    a=[]
    for i in range(len(originais)):
        a.append((originais[i].split('-')))

    #print(len(originais))
    for x in range(0,137):
        print(str(x+2) + "="+str(len(a[x])))
