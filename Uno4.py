
from random import *
from tkinter import *
from PIL import Image, ImageTk


def start():
    global fenprinc
    fenprinc=Tk()
    fenprinc.geometry("1350x766")
    fenprinc.title("Undostres")
    
    image = Image.open("uno.jpg") 
    photo = ImageTk.PhotoImage(image)  
    canvas = Canvas(fenprinc, width = image.size[0], height = image.size[1])  
    canvas.create_image(0,0, anchor = NW, image=photo) 
    canvas.pack()
    Text= Button(fenprinc, text="Commencer la partie", bg="white",relief="raised", font=("Times", "20", "bold"),cursor="heart",command=fenetre_data)
    Text.pack()
    Text_fenprinc= canvas.create_window(1100, 130, window=Text)
    
    fenprinc.mainloop()
    
def melange(paquet):
    """
    Permet de melanger le paquet de cartes
    """
    shuffle(paquet)


def init():
    global mains, ordre_passage, nb_joueurs, nb_cartes
    
    main_jou=[]
    for j in range(0,nb_cartes):
        carte=paquet.pop(randint(1,len(paquet)-1))
        main_jou.append(carte)
    mains[nomjou]= main_jou
    ordre_passage[salade]=nomjou

def init2():
    global sens,dico
    
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
       sens=-sens
    elif text3[0:10]=="passe tour":
        numero_jou=2
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
        return "Erreur"
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

def pioche (paquet):
    """
    Permet de piocher une carte dans la pioche
    """
    carte_pioche=paquet.pop(randint(0,len(paquet)-1))
    return carte_pioche


def piocher(paquet, main_joueur, nombre_cartes):
    """
    Permet de piocher un nombre de cartes donné et de les mettre dans la main d'un joueur
    """
    if len(paquet) < nombre_cartes :
        pioche_vide(paquet, pile_jeu)
    for i in range (nombre_cartes):
        main_joueur.append(pioche(paquet))

def pioche_vide(pioche, pile_jeu):
    """
    Permet de refaire une pioche avec le tas du jeu si celle-ci est vide
    """
    for i in range (len(pile_jeu)-1):
        a=pile_jeu.pop(0)
        pioche.append(a)
        melange(pioche)

def regles_jeu(carte, tas_jeu):
    """
    Vérifie si les règles du jeu sont respectées
    """
    if (couleur(carte) == couleur(tas_jeu[-1])) or (num_carte(carte)== num_carte(tas_jeu[-1])) or ((texte(carte)== "joker") or (texte(tas_jeu[-1])=="joker") and (texte(tas_jeu[-1]) != "+2") and (texte(tas_jeu[-1]) != "+4")) or (texte(carte)== "+4") :
        return True
    else :
        return False

def plus4(tas_jeu):
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
    global paquet, couleur4, actif, compteurplus4,sens, verifprint
    """
    Fait piocher le joueur en cas de besoin
    """
    peut_jouer=True
    compteur_2=True
    text=(texte(tas_jeu[-1]))
    if text[0:2]=="+2":
        compteur_2=False
        for i in main_joueur:
            text2=texte(i)
            if text2[0:2]=="+2" or texte(i)=="+4":
                compteur_2=True
        if compteur_2==False:
            compteur_pioche=plus4(tas_jeu)
            piocher(paquet, main_joueur, compteur_pioche)
            peut_jouer=False

    elif text =="+4":
        compteur_2=False
        for i in main_joueur:
            if texte(i)=="+4":
                compteur_2=True
        if compteur_2==False:
            compteur_pioche=plus4(tas_jeu)
            piocher(paquet, main_joueur, compteur_pioche)
            peut_jouer=False
            if sens == 1:
                prenom=ordre_passage[(actif-1)%nb_joueurs]
            if sens == -1:
                prenom=ordre_passage[(actif+1)%nb_joueurs]
            print("Quelle couleur souhaitez-vous ", prenom, " ? ")
            couleur4=input("")
            dico[tas_jeu[-1]]=couleur4

    else :
        k=0
        for i in main_joueur :
            verifie = regles_jeu(i, tas_jeu)
            if verifie==False:
                k+=1
        if k==len(main_joueur):
            affiche=[texte(i) for i in mains[ordre_passage[actif]]]
            print("Au tour du joueur", ordre_passage[actif], affiche)
            joueur_piocher = input("Vous ne pouvez pas jouer, voulez-vous piocher ? y/n")
            if joueur_piocher == "y":
                piocher(paquet, main_joueur, 1)
                affiche=[texte(i) for i in main_joueur]
                print("Voici votre nouveau jeu : ", affiche)
                verifie=regles_jeu(main_joueur[-1],tas_jeu)
                if verifie==True:
                    peut_jouer=True
                else :
                    peut_jouer=False
                    print("False")
            else :
                print("Vous êtes obligés de piocher")
                piocher(paquet, main_joueur, 1)
                affiche=[texte(i) for i in main_joueur]
                print("Voici votre nouveau jeu : ", affiche)
                verifie=regles_jeu(main_joueur[-1],tas_jeu)
                if verifie==True:
                    peut_jouer=True
                else :
                    peut_jouer=False

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

    print(nb_cartes,nb_joueurs)

def fenetre_nom():
    global dico_noms,fennom
    
    fennom=Tk()
    ordre=Label(text="Entrez le nom des joueurs")
    ordre.pack()
    valider2=Button(fennom, text="Valider", command=programme_principal)
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

    

def programme_principal():
    global nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage,nomjou,salade, actif
    
    dictionnaire_trad={"bleu":"cyan","rouge":"red","vert":"green","jaune":"yellow"}
    paquet =[i for i in range (1,109)]
    melange(paquet)
    tas_jeu=[paquet[0]]
    actif=0
    init2()
    mains={}
    ordre_passage={}
    totalite_cartes={}
    
    for i in range (108):
        totalite_cartes[i]=str(texte(i))
    clefs_cartes=list(totalite_cartes.keys())

    for salade in range(nb_joueurs):
        nomjou=dico_noms[salade].get()
        init()
    
    
    fennom.destroy()
    
    print(texte(tas_jeu[-1]))
    fencarte=Tk()
    
    test2=joue_ou_pioche(mains[ordre_passage[0]], tas_jeu)

    while actif != None:
        affiche=[texte(i) for i in mains[ordre_passage[actif]]]
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
            for i in affiche:
                if i.split()[-1]==i.split()[0]:
                    i=Button(fencarte, text=i, width=15, height=15)
                else :
                    i=Button(fencarte, bg=str(dictionnaire_trad[str(i.split()[-1])]), text=i, width=15, height=15)
                carte=i.config(command=lambda bt=i: ff(bt))
                i.grid(column=colonne, row=3, sticky=E)
                colonne+=1
            #carte=clefs_cartes(carte)# A reprendre
           
            """
            a=mains[ordre_passage[actif]]
            carte=a[carte]
            """
            actif=Tour_jeux(actif, mains[ordre_passage[actif]], tas_jeu, nb_joueurs,carte)
        else :
            actif2=sens_jeu(mains[ordre_passage[actif]], tas_jeu, nb_joueurs, actif)
            actif=actif2

    fencarte.mainloop()
start()
