import numpy as np
import cv2
from decimal import Decimal
#from Similaridade import*
from Descritores import*
import os
from sklearn import metrics
from math import*


class Similaridade():

    def euclidean_distance(self,x,y):
		#print("Usando a distancia euclidana")

		return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

	def manhattan_distance(self,x,y):

		return sum(abs(a-b) for a,b in zip(x,y))


	def minkowski_distance(x,y,p_value):
		return nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),p_value)

	def nth_root(value, n_root):

		root_value  = 1/float(n_root)
		return round (Decimal(value) ** Decimal(root_value),3)

	def cosine_similarity(self,x,y):

		numerator = sum(a*b for a,b in zip(x,y))
		denominator = square_rooted(x)*square_rooted(y)
		return round(numerator/float(denominator),3)

	def square_rooted(x):

		return round(sqrt(sum([a*a for a in x])),3)


	def jaccard_similarity(self,x,y):

		intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
		union_cardinality = len(set.union(*[set(x), set(y)]))
		return intersection_cardinality/float(union_cardinality)
	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
						  for (a, b) in zip(histA, histB)])

		# return the chi-squared distance
		return d


class cortes():
	def __init__(self,name,frame,msec):
		self.name=name
		self.frame=frame
		self.msec=msec

	def printCortesInfo(self):
		print("I:"+ self.name)
		print("MSCE"+ self.msec)


def extract_frames(stri, janela):
	print("----------------\n")
	print("O Nome do video é:"+stri)
	print("O tamanho da Janela é: "+ str(janela))
	cap = cv2.VideoCapture(stri)
	lst=[]

	if(cap.isOpened()):

		total_of_frames=  int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		for x in range(1,total_of_frames,janela):
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			o = cortes(cap.get(cv2.CAP_PROP_POS_FRAMES),gray, cap.get(cv2.CAP_PROP_POS_MSEC))
			lst.append(o)

	return lst

def extract_framesS(stri,janela):
	print("----------------\n")
	print("O Nome do video é:"+stri)
	cap = cv2.VideoCapture(stri)
	lst=[]

	os.mkdir(stri[:len(stri)-4]+"-frames")

	if(cap.isOpened()):

		total_of_frames=  int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

		print(total_of_frames)

		for x in range(1,total_of_frames, janela):

			cap.set(cv2.CAP_PROP_POS_FRAMES, x)

			ret, frame = cap.read()



			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			cv2.imwrite(stri[:len(stri)-4]+"-frames/"+str(x)+".png", gray)

			o = cortes(cap.get(cv2.CAP_PROP_POS_FRAMES),gray, cap.get(cv2.CAP_PROP_POS_MSEC))

			lst.append(o)

	return lst

def take(lst,posic,sec,limiar):
	c= []
	secs=[]
	#pos=[]
	for x in range(0, len(lst)-1):
		#if((lst[x].all())!=None):
		s= Similaridade()

		print(lst[x])

		if s.euclidean_distance(lst[x],lst[x+1])> limiar:
			c.append(lst[x])
			secs.append(sec[x])

	print("Limiar:"+str(limiar))
	print("Total Cortes:"+str(len(secs)) )
	print(secs)
	print("----------------\n")
	return (c,secs)

def list_of_sift(lst):
	lsty=[]
	posic=[]
	sec= []
	for x in range(0,len(lst)):
		desc = Descritores()
		a =desc.Sift((lst[x].frame))
		#if(a==None):
		#	x=x+1
		#else:	
		lsty.append(a)
		posic.append(lst[x].name)
		segundos= (lst[x].msec)
		sec.append(segundos)

	return (lsty	, posic, sec)

def list_of_surf(lst):
	lsty=[]
	posic=[]
	sec= []
	for x in range(0,len(lst)):
		desc = Descritores()
		a =desc.Surf((lst[x].frame))
		lsty.append(a)
		posic.append(lst[x].name)
		segundos= (lst[x].msec)
		sec.append(segundos)

	return (lsty	, posic, sec)

def list_of_hist(lst):
	lsty=[]
	posic=[]
	sec= []
	for x in range(0,len(lst)):
		desc = Descritores()
		a =desc.histograma((lst[x].frame))
		lsty.append(a)
		posic.append(lst[x].name)
		segundos= (lst[x].msec)
		sec.append(segundos)

	return (lsty	, posic, sec)


def list_of_bic(lst):
	lsty=[]
	posic=[]
	sec= []
	for x in range(0,len(lst)):
		desc = Descritores()
		a =desc.bic(lst[x].frame)

		lsty.append(a)

		posic.append(lst[x].name)

		segundos= (lst[x].msec)
		sec.append(segundos)
	return lsty, posic, sec

def main():
	top= os.listdir('/home/katiely/Vídeos/Take/Base_Videos')
	top.sort()
	lista=[]
	lst=extract_frames('/home/katiely/Vídeos/Take/Base_Videos/Amy Winehouse - Rehab.mp4',10)
	# for video in top[1]:
	# 	lista.append(extract_frames('/home/katiely/Vídeos/Take/Base_Videos/'+video,10))
	print(len(lst))

	print("-------------------------------------------------------")
	(sift_l, posic, sec)= list_of_sift(lst)

#(c,secs)=take(sift_l,posic,sec,1)
#print(sift_l)
# print(secs)
# print(len(c))
# tops = []
# for x in lista:
# 	tops.append(x)
# with open('meuTEst.txt','a+') as arq:
# 		#salvar= str(secs)
# 		#so para tirar as chavinhas da  lista com os meninos cortes
# 		#salvar = salvar[1:len(salvar)-1]
# 		arq.write(str(tops))


#main()
def videosTake():
	top= os.listdir('/home/katiely/Vídeos/Take/Base_Videos')
	top.sort()
	#print(top)
	limiar = 40000
	lista=[]
	for video in top:
		lista = extract_frames('/home/katiely/Vídeos/Take/Base_Videos/'+video,10)

		(l,p,sec)= list_of_hist(lista)

		(c,secs)=take(l,p,sec,limiar)
		#with open('histOrdem.txt','a+') as file:
		#file.write(video+'\n')
		with open('hist_300.txt','a+') as arq:
			salvar= str(secs)
			#so para tirar as chavinhas da  lista com os meninos cortes
			salvar = salvar[1:len(salvar)-1]
			arq.write(salvar+'\n')


videosTake()


