
from random import *
from tkinter import *
#from PIL import Image, ImageTk
from tkinter import messagebox


def start():
    global fenprinc
    fenprinc=Tk()
    fenprinc.geometry("1350x766")# redimension de la fenêtre
    fenprinc.title("Undostres") #renommer la fenêtre
    """
    image = Image.open("uno.gif")
    print("wesh")
    photo = PhotoImage('Users\GE3MS\Desktop\Manon mon seul Amour\monuno.gif')
    print("alors")
    """
    canvas = Canvas(fenprinc)
    """
    canvas.create_image(0,0, anchor = NW, image=photo)
    print("pouloulou")
    canvas.image=photo
    print("yolo")
    """
    canvas.pack()
    Text= Button(fenprinc, text="Commencer la partie", bg="white",relief="raised", font=("Times", "20", "bold"),cursor="heart",command=fenetre_data)
    Text.pack()
    #Text_fenprinc= canvas.create_window(1100, 130, window=Text)
    fenprinc.mainloop()
    
def melange(paquet):
    """
    Permet de melanger le paquet de cartes
    """
    shuffle(paquet)


def init():
    """
    Creation mains de joueurs et de l'ordre de passage
    """
    global mains, ordre_passage, nb_joueurs, nb_cartes
    
    main_jou=[]
    for j in range(0,nb_cartes):
        carte=paquet.pop(randint(1,len(paquet)-1))
        main_jou.append(carte)
    mains[nomjou]= main_jou
    ordre_passage[salade]=nomjou

def init2():
    """
    Crée le dictionnaire qui contient les couleurs en fonction de l'indice de la carte, initialise le sens et l'actif.
    """
    global sens,dico, actif
    
    actif=0
    
    dico={}
    dico[0]="nul"
    for i in range (1,26):
        dico[i]="rouge"
    for i in range(26,51):
        dico[i]="bleu"
    for i in range(51,76):
        dico[i]="jaune"
    for i in range (76,101):
        dico[i]="vert"
    for i in range (101,109):
        dico[i]=None

    sens =1

def sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif):
    global sens
    """
    Renvoie le numéro du joueur suivant
    """
    numero_jou=1
    text3=texte(tas_jeu[-1])
    if text3[0:15]=="changement_sens":
       sens=-sens #change le sens si jamais la carte est un changement de sens
    elif text3[0:10]=="passe tour":
        numero_jou=2 #fait passer 2 joueurs au lieu d'un lorsque la carte est un passe-tour
    actif = (actif+sens*numero_jou)%nb_joueurs-1
    return actif+1

def couleur(indice):
    """
    Permet d'obtenir la couleur d'une carte donnee par son indice.
    """
    return dico[indice]

def num_carte(indice):
    """
    Permet d'obtenir le numero d'une carte en fonction de son indice.
    +2=10
    chgt de sens =11
    passe tour = 12
    """
    if 108 < indice or indice < 1:
        return "Erreur" #Permet de déceler une erreur car ces cartes n'existent pas
    k=1
    for i in range (1,indice+1):
        if k==26 or k==51 or k==76 :
            k=1 
        k+=1

    Paszéro= True
    while Paszéro:
        if k%2==0 :
            num=int(k/2-1)
            Paszéro=False
        else :
            num=int(k//2)
            if num==0:
                k+=1
                Paszéro=False
            else :
                Paszéro = False
    return num

def texte(indice):
    """
    Reçoit l'indice d'une carte et renvoie le texte complet correspondant
    """
    numero= num_carte(indice)
    if numero == 10 :
        numero="+2"
    elif numero == 11:
        numero = "changement_sens"
    elif numero==12:
        numero = "passe tour"
    elif 100<indice<105:
        numero = "joker"
    elif 104 < indice <109:
        numero = "+4"

    if couleur(indice)== None:
        text= str(numero)
    else :
        text= str(numero) + " " + couleur(indice)
    return text

def regles_jeu(carte, tas_jeu):
    """
    Vérifie si les règles du jeu sont respectées
    """
    if (couleur(carte) == couleur(tas_jeu[-1])) or (num_carte(carte)== num_carte(tas_jeu[-1])) or ((texte(carte)== "joker") or (texte(tas_jeu[-1])=="joker") and (texte(tas_jeu[-1]) != "+2") and (texte(tas_jeu[-1]) != "+4")) or (texte(carte)== "+4") :
        return True
    else :
        return False

def pioche (paquet):
    """
    Permet de piocher une carte dans la pioche
    """
    carte_pioche=paquet.pop(randint(0,len(paquet)-1))
    return carte_pioche


def piocher(paquet, main_joueur, nombre_cartes=1):
    global fencarte
    """
    Permet de piocher un nombre de cartes donné et de les mettre dans la main d'un joueur
    """
    if len(paquet) < 1 :
        pioche_vide(paquet, pile_jeu)
    for i in range(nombre_cartes):
        main_joueur.append(carte_archive)
        
def piocher2():
    global fencarte
    """
    Permet de piocher un nombre de cartes donné et de les mettre dans la main d'un joueur
    """
    if len(paquet) < 1 :
        pioche_vide(paquet, pile_jeu)
    carte_archive=pioche(paquet)
    mains[ordre_passage[actif]].append(carte_archive)
    if regles_jeu(carte_archive, tas_jeu):
        a=Button(fencarte)
        a.grid(row=3, column=9)
            
        
def pioche_vide(pioche, pile_jeu):
    """
    Permet de refaire une pioche avec le tas du jeu si celle-ci est vide
    """
    for i in range (len(pile_jeu)-1):
        a=pile_jeu.pop(0)
        pioche.append(a)
        melange(pioche)



def nbpioche(tas_jeu):
    """
    Retourne le nombre de cartes que doit piocher le joueur
    """
    i=-1
    compteurpioche=0
    nom=texte(tas_jeu[i])
    while nom[0:2] == "+2" or nom=="+4":
        if nom[0:2]=="+2":
            compteurpioche=compteurpioche+2
        else:
            compteurpioche=compteurpioche+4
        
        if tas_jeu[i]!=tas_jeu[0]:
            i-=1
            nom=texte(tas_jeu[i])
        else:
            break
    return compteurpioche


def joue_ou_pioche(main_joueur, tas_jeu):
    global paquet, couleur4, actif,sens, verifprint
    """
    Fait piocher le joueur en cas de besoin
    """
    peut_jouer=True #va être retourné, précise si le joueur peut encore jouer ou non
    compteur_2=True
    if texte(tas_jeu[-1])[0:2]=="+2":
        peut_repliquer=False
        for i in main_joueur:
            if texte(i)[0:2]=="+2" or texte(i)=="+4":
                peut_repliquer=True #Si le joueur possède un +2 ou un +4 dans son jeu, il peut jouer
        if not peut_repliquer:
            compteur_pioche=nbpioche(tas_jeu)#determine le nombre de cartes a piocher
            piocher(paquet, main_joueur, compteur_pioche) #fait piocher la joueur
            peut_jouer=False

    elif texte(tas_jeu[-1]) =="+4":
        peut_repliquer=False
        for i in main_joueur:
            if texte(i)=="+4":
                peut_repliquer=True
        if not peut_repliquer:
            compteur_pioche=nbpioche(tas_jeu)
            piocher(paquet, main_joueur, compteur_pioche)
            peut_jouer=False
            if sens == 1:
                prenom=ordre_passage[(actif-1)%nb_joueurs]
            if sens == -1:
                prenom=ordre_passage[(actif+1)%nb_joueurs]
            Tu_as_cette_couleur=False
            while not Tu_as_cette_couleur:
                print("Quelle couleur souhaitez-vous ", prenom, " ? ")
                couleur4=input("")
                for w in mains[ordre_passage[actif]]:
                    if texte([w]).split()[-1]==couleur4 or texte([w]).split()[0]=="+4" or texte([w]).split()[0]=="joker":
                        Tu_as_cette_couleur=True               
            dico[tas_jeu[-1]]=couleur4

    return peut_jouer


def carte_a_jouer(main_joueur, tas_jeu, carte):
    global actif
    """
    Verifie si le joueur peut jouer la  carte
    """
    ok=joue_ou_pioche(main_joueur, tas_jeu)
    ok2=False
    if ok:
        ok2=regles_jeu(carte, tas_jeu)
        while ok2==False:
            print(ok2, carte)
            carte=int(input("Choisissez une autre carte : "))
            a=mains[ordre_passage[actif]]
            carte=a[carte]
            ok2=regles_jeu(carte, tas_jeu)
            print(ok2)
        return carte
    else :
        return False

def test_victoire(main_joueur):
    """
    Teste si un joueur a gagné, renvoie True si il a gagné
    """
    if len(main_joueur)==0:
        print("VOUS AVEZ GAGNE !!!!!!!! \n Fin de la partie ")
        return True
    else :
        return False

def Tour_jeux(actif, main_joueur, tas_jeu, nb_joueurs,carte):
    global mains, ordre_passage
    """
    Renvoie l'actif si jamais personne n'a gagné
    """
    test=carte_a_jouer(main_joueur, tas_jeu, carte)
    if test != False :
        print(actif)
        print(main_joueur)
        carte2=main_joueur.pop(main_joueur.index(test))
        tas_jeu.append(carte2)
    vict=test_victoire(main_joueur)
    if vict:
        return None
    else :
        actif=sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif)
        return actif

def okE(key):
    global joueurs
    touche=key.keysym
    if touche=="Return":
        joueurs=entree.get()

def fenetre_data():
    global entree, nb_cartes,nb_joueurs,fenjeu,entree, entree2
    
    fenjeu=Tk()
    fenjeu.title("Données de base")
    texte_nb_joueurs=Label(fenjeu,text="Combien de joueurs ? ")
    texte_nb_joueurs.pack()
   
    entree=Entry(fenjeu)
    entree.pack()
    texte_nb_cartes=Label(fenjeu,text="Combien de cartes par main ? ")
    texte_nb_cartes.pack()
    entree2=Entry(fenjeu)
    entree2.pack()
    valider=Button(fenjeu, text="Valider", command=programme1)
    valider.pack()
    
    entree.focus_set()
    fenjeu.bind("<Return>",okE)


def fenetre_nom():
    global dico_noms,fennom
    
    
    fennom=Tk()
    fennom.title("Fenetre de jeu")
    ordre=Label(text="Entrez le nom des joueurs")
    ordre.pack()
    valider2=Button(fennom, text="Valider", command=initinit)
    valider2.pack()
    dico_noms={}
    for i in range (nb_joueurs):
        dico_noms[i]="nom"+str(i)
    for i in range (nb_joueurs):
        dico_noms[i]=Entry(fennom)
        dico_noms[i].pack()

def programme1():
    global nb_joueurs, nb_cartes
    
    nb_joueurs=int(entree.get())
    nb_cartes=int(entree2.get())
    fenjeu.destroy()
    fenprinc.destroy()
    fenetre_nom()

def ff(bt):
    global carte
    carte=bt.cget("text")
    print("La arte est :",carte)
    programme_principal()

def initinit():
    global  nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage,nomjou,salade, actif, totalite_cartes, carte, fencarte, dictionnaire_trad, affiche
    paquet =[i for i in range (1,109)]
    melange(paquet)
    tas_jeu=[paquet[0]]
    
    init2()
    mains={}
    ordre_passage={}
    

    for salade in range(nb_joueurs):
        nomjou=dico_noms[salade].get()
        init()
    
    
    fennom.destroy()
    
    print(texte(tas_jeu[-1]))
    
    
    test2=joue_ou_pioche(mains[ordre_passage[0]], tas_jeu)
    affiche=[texte(i) for i in mains[ordre_passage[actif]]]
    totalite_cartes={}
    dictionnaire_trad={"bleu":"cyan","rouge":"red","vert":"green","jaune":"yellow"}
    fencarte=Tk()
    fencarte.title("Fenetre espion")
    for i in range (108):
        totalite_cartes[i]=str(texte(i))
    clefs_cartes=list(totalite_cartes.keys())
    creer_cartes()

def creer_cartes():
    global  nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage,nomjou,salade, actif, totalite_cartes, carte, fencarte, affiche, showinfo
    
    
    messagebox.showinfo("Changement", "Au tour du joueur : " + ordre_passage[actif]) #fenetre de changement de tour
    fencarte.destroy() #Destruction de la fenêtre de jeu
    fencarte=Tk()
    fencarte.title("Fenetre de jeu carte")
    if couleur(tas_jeu[-1])==None:
        Carte_tas_jeu=Button(fencarte, text=str(texte(tas_jeu[-1])), width=15, height=15)
    else:
        Carte_tas_jeu=Button(fencarte, bg=str(dictionnaire_trad[str(couleur(tas_jeu[-1]))]), text=str(texte(tas_jeu[-1])), width=15, height=15)
    Carte_tas_jeu.grid(column=1, row=1)
    print("Carte dessus paquet : ",texte(tas_jeu[-1]))
    test2=joue_ou_pioche(mains[ordre_passage[actif]], tas_jeu)
    if test2:
        print("Au tour du joueur", ordre_passage[actif], affiche)
        au_tour=Label(fencarte, text="Au tour du joueur "+str(ordre_passage[actif]))
        
        au_tour.grid(column=1, row=2)
        colonne=1
        affiche=[texte(i) for i in mains[ordre_passage[actif]]]
        for i in affiche:
            if i.split()[-1]==i.split()[0]:
                i=Button(fencarte, text=i, width=15, height=15)
            else :
                i=Button(fencarte, bg=str(dictionnaire_trad[str(i.split()[-1])]), text=i, width=15, height=15)
            carte=i.config(command=lambda bt=i: ff(bt))
            i.grid(column=colonne, row=3, sticky=E)
            colonne+=1
        bouton_pioche=Button(fencarte, text="Piocher", command=piocher2)
        bouton_pioche.grid(row=3, column=8)
            
    else :
        actif2=sens_jeu(mains[ordre_passage[actif]], tas_jeu, nb_joueurs, actif)
        actif=actif2
        creer_cartes()
    

def programme_principal():
    global nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage,nomjou,salade, actif, carte
    
    print("carte", carte)
    for k in totalite_cartes:
        if totalite_cartes[k]==carte:
            carte=k
            while not carte in mains[ordre_passage[actif]]:
                carte+=1
            print(carte)
    actif=Tour_jeux(actif, mains[ordre_passage[actif]], tas_jeu, nb_joueurs,carte)
    
    creer_cartes()
    fencarte.mainloop()

    
start()
