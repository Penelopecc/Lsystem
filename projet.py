from turtle import *
import os.path
from random import *

#recup des regles
#contient = avec guillemet
def rules(x):
   lignes2=lignes
   lignes2[x]=lignes2[x][lignes2[x].find("=")+1:]
   for i in range(len(lignes2)-1,-1,-1):
       lignes2[i]=lignes2[i].strip(' \t\n\r')
       if lignes2[i][:1] != '"' :
           del lignes2[i]
   for i in range(len(lignes2)):
       lignes2[i]=lignes2[i].replace('"',"")
   return(lignes2)

def verifMotClef(mot):
    for i in lignes:
        if i.find(mot) > -1:
            return(True)
    return(False)

#Teste l'axiome
def testAxiome(axiome):
    test=list(axiome)
    for i in test:
        if (i == "a") or (i == "b") or (i == "-") or (i == "+") or (i == "[") or (i == "r") or (i == "c") or (i == "g") or (i == "m"):
            return(True)
        else:
            return(False)

#retrouve les arguments
def argument(mot):
   for x in range(len(lignes)):
       a=lignes[x].find("=")
       if a>=0:
           motclef=lignes[x][:a]
           motclef=motclef.strip(' \t\n\r')
           if mot==motclef:
               if mot=="regles":
                   return(rules(x))
               arg=lignes[x][a+1:]
               arg=arg.strip(' \t\n\r')
               arg=arg.replace('"','')
               arg=arg.strip(' \t\n\r')
               return(arg)

#affecte les regles
def generateur(lsystem,regles):
   decoup=list(lsystem)
   for x in range(len(decoup)):
       for i in regles:
           if i[0] == decoup[x]:
               decoup[x]=decoup[x].replace(i[0],i[2:])
   lsystem=""
   for x in decoup:
       lsystem=str(lsystem+x)
   return(lsystem)

#affecte les regles autant de fois qu'il y a de niveau
def main(niveau,lsystem):
   for i in range(1,niveau+1):
       lsystem=generateur(lsystem,regles)
   return(lsystem)

#pour enlever.py
def sanspoint(strings):
   string_final = ""
   for string in strings:
       if string!='.':
           string_final += string
       else:
           break
   return string_final

def useColor():
    color=str(input("Voulez vous de la couleur (yes/no) ? :"))
    if color == 'yes':
        return(True)
    else:
        return(False)

'''dessine
b ---> pen up
+ ---> turn right
- ---> turn left
* ---> return
[ ---> ouvre branch
] ---> ferme branch
H ---> return home
a ---> pen down
m ---> color brown
g ---> color green
r ---> color red
l ---> color blue
y ---> color yellow
n ---> color black
u ---> color random'''
def dessine(dfile):
       f = open(dfile,'w')
       f.write("from turtle import *\nspeed(0)\npensize("+str(taille/5)+")\n")
       f.write("a=[]\n\n")
       if useColor():
           couleur=["red","blue","black","yellow","pink","purple","grey","orange"]
       else:
           couleur=["black"]
       compteur=0
       for i in range (len(fonction)):
           if fonction[i]=="b":
               f.write("pu();\nfd("+str(taille) +");\n")
           if fonction[i]=="+":
               f.write("right("+str(angle)+");\n")
           if fonction[i]=="-":
               f.write("left("+str(angle)+");\n")
           if fonction[i]=="*":
               f.write("right(180);\n")
           if fonction[i]=="[":
               f.write("a.append([pos(),heading()]);\n")
           if fonction[i]=="]":
               f.write("pu()\nb=a.pop()\nsetheading(b[1])\ngoto(b[0]);\n")
           if fonction[i]=="l":
               f.write("pencolor('blue');\n")
           if fonction[i]=="a":
               f.write("pd();\nfd("+str(taille)+");\n")
           if fonction[i]=="c":
               f.write("pd();\nfd("+str(taille)+");\n")
           if fonction[i]=="m":
               f.write("pencolor('brown');\n")
           if fonction[i]=="g":
               f.write("pencolor('green');\n")
           if fonction[i]=="r":
               f.write("pencolor('red');\n")
           if fonction[i]=="y":
               f.write("pencolor('yellow');\n")
           if fonction[i]=="n":
               f.write("pencolor('black');\n")
           if compteur%10 == 0:
               f.write("pencolor('"+choice(couleur)+"')\n")

       f.write("done();")
       f.close()
       efile=sanspoint(dfile)
       new_module = __import__(efile)
       '''import sav importe n'est pas compatible avec une variable donc j’ai trouvé un autre moyen'''

def entree():
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("-i",help="fichier d'entrée")
   parser.add_argument("-o",help="fichier de sortie")
   args = parser.parse_args()
   if (args.i ==''or args.i==None):
       f=input("Quel est votre fichier d'entrée? : ")
       if f=='':
           f='config.txt'
           print(f)
   else:
       f=args.i
   fsortie = 'sav.py'
   if (args.o !='' and args.o !=None):
       fsortie = args.o
   return (f,fsortie)

#main
fich = entree()
if os.path.exists(fich[0]):
   fichier=open(fich[0],"r")
   lignes=fichier.readlines()
   fichier.close()
   if (verifMotClef("axiome") and verifMotClef("angle") and verifMotClef("niveau") and verifMotClef("taille") and verifMotClef("regles")) == True:
       axiome=str(argument("axiome"))
       niveau=int(argument("niveau"))
       angle=float(argument("angle"))
       taille=int(argument("taille"))
       regles=argument("regles")
       if taille>0:
           if testAxiome(axiome) == True :
                if ((type(angle) == float) or (type(angle) == int)) and (angle != 0):
                    lsystem=axiome
                    fonction=main(niveau,lsystem)
                    print(main(niveau,lsystem))
                    dessine(fich[1])
           else:
                print("L'axiome n'est pas valide")
       else:
            print("Erreur, la taille est négative")
   else:
        print("Il manque un mot clef")
else:
   print("Erreur, le fichier " +fich[0]+ " n'existe pas!")
