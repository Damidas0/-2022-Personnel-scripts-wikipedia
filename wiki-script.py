

import os


#Pour une page description de la forme 
def remplit_desc(fichier_desc, fichier_page) : 
    log=open("log.txt", 'w', encoding = 'UTF-8')
    fichier = open("output.txt", 'w', encoding='UTF-8')
    f =  open(fichier_desc, 'r', encoding='UTF-8')  #recup txt pour description 
    l_fichier_desc = f.read()  
    tab_fichier_desc = l_fichier_desc.split("\n\n")  #split par grp de nom pour description 
    while('' in tab_fichier_desc) : 
        tab_fichier_desc.remove('')

    #On veut mtn parcourir en réécrivant le texte du wikipedia pour y ajouter les descriptions 
    fichier_page = open(fichier_page, 'r', encoding='UTF-8') 
    i=0
    next_est_titre = False
    change_desc_c = 0
    for line in fichier_page : #On parcours en réécrivant comme on le veut 
        if (i>=len(tab_fichier_desc)) : 
            fichier.write(line)
            continue
        
        if(next_est_titre) : #Si on a déterminé que ct un titre 
            if line =="|\n" : 
                fichier.write("|")
                continue
            else : 
                next_est_titre = False
                fichier.write(line)
                nom = normalise(line)
                
            if(meme_nom_2(nom, tab_fichier_desc[i])) :  
                log.write("Iteration sur : " + nom + " " + tab_fichier_desc[i].split("\t")[-1] +"\n")
                change_desc_c = 1
            continue
            
        if(change_desc_c >0) : 
            if (change_desc_c == 1) : 
                if tab_fichier_desc[i].split("\t")[-1] != "Euh ton prog marche ap" : 
                    fichier.write("| " + tab_fichier_desc[i].split("\t")[-1]+"\n")
                i+=1
                change_desc_c = 0
                continue
            else : 
                fichier.write(line)
                change_desc_c -=1 
                continue
        else :
            fichier.write(line)
        
        if line == "|-\n" : 
            next_est_titre = True


def meme_nom_2(nom, ligne_nom) : 
    tab_ligne = ligne_nom.split("\t")
    nom2 = tab_ligne[0]
    return (nom2 in nom or nom2 in nom)



def remplit_img(fichier_img, fichier_page) : 
    log=open("log.txt", 'w', encoding = 'UTF-8')
    fichier = open("output.txt", 'w', encoding='UTF-8')
    f =  open(fichier_img, 'r',encoding='UTF-8')  #recup txt img 
    l_fichier_img = f.read()  
    tab_fichier_img = l_fichier_img.split("\n")  #split par grp de nom pour img 
    while('' in tab_fichier_img) : 
        tab_fichier_img.remove('')
    #On veut mtn parcourir en réécrivant le texte du wikipedia pour y ajouter les images
    #Pour chaque ligne si la ligne est égale à un bateau ET que le tableau 
    #Boucle while 
    fichier_page = open(fichier_page, 'r', encoding='UTF-8') 
    i=0
    c = True
    while (i<len(tab_fichier_img)) : #A enlever y sert à rien
        next_est_titre = False
        change_img_c = 0 #Compteur pour savoir dans cb d'image on voit changer
        for line in fichier_page : #On parcours en réécrivant comme on le veut 
            if (i>=len(tab_fichier_img)) : 
                fichier.write(line)
                continue
            
            if(next_est_titre) : #Si on a déterminé que ct un titre 
                if line =="|\n" : 
                    fichier.write("|")
                    continue
                else : 
                    next_est_titre = False
                    fichier.write(line)
                    nom = normalise(line)
                    
                    #fichier.write ("|[["+nom+"]]\n") 
                    if(meme_nom(nom, tab_fichier_img[i])) :
                        log.write("Iteration sur : " + nom + " " + tab_fichier_img[i].split("\t")[-1] +"\n")
                        change_img_c = 2
                    continue
            if(change_img_c >0) : 
                if (change_img_c == 1) : 
                    if tab_fichier_img[i].split("\t")[-1] == "Euh ton prog marche ap" : 
                        fichier.write("| style=\"text-align:center;\" | [[Fichier:Defaut.svg|120px]] \n")
                    else : 
                        fichier.write("| style=\"text-align:center;\" | " + tab_fichier_img[i].split("\t")[-1]+"\n")
                    i+=1
                    change_img_c = 0
                    continue
                else : 
                    fichier.write(line)
                    change_img_c -=1 
                    continue
            else :
                fichier.write(line)
            
            if line == "|-\n" : 
                next_est_titre = True
                    
                
        
def normalise(ligne) : 
    mot =""
    for lettre in ligne : 
        if (lettre != "|" and lettre!= "\n" and lettre!= "[" and lettre!= "]" ):
            mot += lettre
    return mot


def meme_nom(nom, ligne_nom_page) : 
    nom2 ="" 
    tab_ligne = ligne_nom_page.split(" ")
    for mot in tab_ligne: 
        print(mot)
        if mot[:5] == "style" : 
            break
        else : 
            nom2 += mot +" "
    nom2 = nom2[:-1]
    return (nom2 in nom or nom2 in nom)



def change_param_tab(nom_tete, nouveaux_parametres, nouveau_nom = -3) : #change un param précis
    if (nouveau_nom == -3) : 
        nouveau_nom = nom_tete
    fichier_page = open("input.txt", 'r', encoding='UTF-8') 
    fichier = open("output.txt", 'w', encoding='UTF-8')
    
    #On veut mtn parcourir en réécrivant avec un nv param pour chaque tab
    #Pour chaque ligne si le titre correspon on réécrit
    for line in fichier_page : #On parcours en réécrivant comme on le veut 
        if(nom_tete in line) : 
            fichier.write("! " + nouveaux_parametres + " | " +nouveau_nom+"\n")
        else : fichier.write (line)


def change_param_tableau(nouveaux_parametres) :
    fichier_page = open("input.txt", 'r', encoding='UTF-8') 
    fichier = open("output.txt", 'w', encoding='UTF-8')
    
    #On veut mtn parcourir en réécrivant avec un nv param pour chaque tab
    #Pour chaque ligne si le titre correspon on réécrit
    for line in fichier_page : #On parcours en réécrivant comme on le veut 
        if("{| class=\"wikitable" in line) :
            line = line.replace("\n", "")
            fichier.write(line +" "+ nouveaux_parametres + "\n")
        else : fichier.write (line)
       

def ameliore_accessibilite_img(num_colonne, taille=1):
    fichier_page = open("input.txt", 'r', encoding='UTF-8') 
    fichier = open("output.txt", 'w', encoding='UTF-8')
    
    #On veut mtn parcourir en réécrivant avec un nv param pour chaque tab
    #Pour chaque ligne si le titre correspon on réécrit
    compteur = 0
    for line in fichier_page : #On parcours en réécrivant comme on le veut 
        compteur +=1
        if ("|-" in line) : 
            compteur =0

        if(compteur==num_colonne) :
            #if ("redresse" in line) : 
            #    if ("redresse=" in line) :       
            #        print("a")#JEN SUIS LA
            if (taille !=1) : line.replace("]]", "redresse="+taille+"]]")
            else : line.replace("]]", "redresse]]")

            if "Defaut.svg" in line : 
                fichier.write("|\n")
        else : fichier.write(line)

        
        



#On applique nos paramètres au driver 
#driver = webdriver.Chrome(executable_path = "chromedriver.exe")
#driver.get("https://fr.wikipedia.org/wiki/Liste_des_types_de_bateaux")


ameliore_accessibilite_img(3)
#change_param_tableau("style=\"width:100%;\"")
#change_param_tab("Description", "style=\"width:60%;\"", "Description")
#remplit_desc("Bato/wikidesc.txt", "Bato/input.txt")
#remplit_img("wikimage.txt", "input.txt")
#remplit_img("wikimage.txt" ,"input.txt")
#fichier = open("input.txt", encoding ='UTF-8', mode='r')
#txt = fichier.read()
#print(txt)
#passage_tab_page(txt)


    