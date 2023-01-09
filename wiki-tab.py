#Ce script permet de passer des listes wikipédias en tableau 

def passage_tab_point(texte) : 
    fichier = open("wiki.txt", encoding='UTF-8', mode = 'w')
    fichier.write("{| class=\"wikitable\" \n! style=\"width:150px;\" |  \
    Type \n! style=\"width:250px;\" | Description succincte \n! style=\"width:150px;\" | Image\n")

    tab = texte.split("•")
    i=0
    for word in tab : 
        if (i != 0) : 
            word = word[2:] #remove "\n" (qd au début !)
        fichier.write ("|-\n|"+word+"\n|\n|")
    fichier.write("\n|}")
    fichier.close()


def passage_tab_etoile(texte, fichier) : #pour les listes à base de *
    fichier.write("{| class=\"wikitable\" \n! style=\"width:150px;\" |  \
    Nom \n! style=\"width:250px;\" | Description \n")
    tab = texte.split("*")
    for word in tab : 
        if ("\n" in word) :
            word = word[:-1]
        if ("[[" not in word) : 
            fichier.write ("\n|-\n|[["+word+ "]]\n|")
        else:
            fichier.write("\n|-\n|"+word+ "\n|")
    fichier.write("\n|}\n")


def passage_tab_page(txt, nom_fichier_output) : #Pour tout une page passe les listes en tableau
    fichier = open(nom_fichier_output +".txt", encoding='UTF-8', mode = 'w')
    tab = txt.split("==")
    #Pour chaque catégorie (séparée par des titre "==")
    for ligne in tab : 
        try :
            if (ligne[1][0]=="*" ): 
                passage_tab_etoile(ligne, fichier)
            elif(ligne[2][0]=="*") : 
                passage_tab_etoile(ligne, fichier)
            else : 
                fichier.write("==" + ligne + "==\n")
        except : 
            pass