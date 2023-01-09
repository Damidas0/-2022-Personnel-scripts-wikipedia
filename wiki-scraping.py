from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from time import sleep


LISTE_EXCEPTION = ["https://commons.wikimedia.org/wiki/File:Discobolus_icon.png?uselang=fr", \
        "https://commons.wikimedia.org/wiki/File:Fairytale_warning.png?uselang=fr",\
        "https://commons.wikimedia.org/wiki/File:Lindisfarne_StJohn_Knot2_3.svg?uselang=fr",\
        "https://commons.wikimedia.org/wiki/File:Clio1_-_2.png?uselang=fr"]


       
        
def recup_desc(driver) : #va chercher les descriptions des pages associées pour un tableau 
    list_table = driver.find_elements(By .CLASS_NAME, 'wikitable')
    file = open("wikidesc.txt", encoding='UTF-8', mode='w')
    for table in list_table : #on recup ttes les tables
        i=0
        lignes = table.find_elements(By .TAG_NAME, 'tr')
        for l in lignes : #on regarde chaque ligne de la table
            i+=1
            if (i == 1) : #On itére par sur l'entête du tableau
                continue 

            est_new = l.find_elements(By .CLASS_NAME, 'new')
            if (est_new != []):#verif si il existe une page associée
                print ("Pas de page associée", l.text)
                continue
                
            if (len(l.text.split(" "))>5) : #verif si une descrption est déjà mise
                print ("Il y a déjà une déscription pour : ", l.text)
                continue
            
            print("\n Iteration sur ", l.text)

            try :
                nom = l.find_element(By .TAG_NAME, 'td').text
            except : 
                pass
            
            try :
                lien = l.find_element(By .TAG_NAME, 'a')
                txt = va_chercher_txt(lien.get_attribute('href'))
                file.write(nom +"\t")#ajout début de ligne
                print(txt)
                file.write(txt)
                file.write("\n\n")
            except : 
                pass


def va_chercher_txt(lien) : 
    options = Options()
    options.headless = True
    #A corriger, faire seulement chrome option
    driver = webdriver.Chrome(options=options, executable_path = "chromedriver.exe")
    driver.get(lien)

    coeur_page = driver.find_element(By .ID, "mw-content-text")
    tab_exclu = determine_txt_exclusion(coeur_page)
    tab_paragraphe_wikimedia = coeur_page.find_elements(By .TAG_NAME, 'p')
    description = ""
    i=0
    nb_ligne = 0
    while (i<len(tab_paragraphe_wikimedia) and nb_ligne <= 2) : #on va recup le text qui nous interesse
        if (tab_paragraphe_wikimedia[i].text not in tab_exclu) : 
            nb_ligne +=1
            description += tab_paragraphe_wikimedia[i].text
        i+=1
    return description      

def determine_txt_exclusion(driver) : #Renvoi une liste des paragraphes ne décrivant pas le corps de la page
    CLASS_EXCLU = ["bandeau-cell"]
    TAG_EXCLU = ["table"]
    liste_c_ban = [] 
    liste_p_ban = [] #Texte a remplir manuellement
    liste_txt_ban = []
    for exclu in CLASS_EXCLU : 
        liste_c_ban += driver.find_elements(By .CLASS_NAME, exclu)
    for exclu in TAG_EXCLU : 
        liste_c_ban += driver.find_elements(By .TAG_NAME, exclu)
    for e in liste_c_ban : 
        liste_p_ban += e.find_elements(By .TAG_NAME, 'p')
    for p in liste_p_ban :
        liste_txt_ban.append(p.text)
    return liste_txt_ban


#Fonction pour aller chercher des images              
def recup_img(driver, nb_colonnes=3) : #va chercher les images pour un tableau 
    list_table = driver.find_elements(By .CLASS_NAME, 'wikitable')
    file = open("wikimage.txt", encoding='UTF-8', mode='w')
    
    for table in list_table : #on recup ttes les tables
        print(table.text)
        i=0
        lignes = table.find_elements(By .TAG_NAME, 'tr')
        for l in lignes : #on regarde chaque ligne de la table
            print(l.text)
            i+=1
            if (i == 1) :
                continue 

            est_new = l.find_elements(By .CLASS_NAME, 'new')
            
            if (est_new != []):#verif si il existe une page associée
                print ("Pas de page associée", l.text)
                continue

            img = l.find_elements(By .CLASS_NAME, 'image')

            if (img != []) : #verif si une image est déjà mise
                if( (img[0].find_element(By .TAG_NAME, 'img').get_attribute('alt')) != "Defaut.svg") :
                    print ("Y A UN IMAGE DEJA pour ", l.text)
                    continue
                else : 
                    print("Image par défaut pour", l.text)

            nb_case = len(l.find_elements(By .TAG_NAME, 'td'))
            if (nb_case != nb_colonnes) : #sécurité pck chiant
                continue

            print("\n\n\n\n\n", "Iteration sur ", l.text)

            try :
                nom = l.find_element(By .TAG_NAME, 'td').text
            except : 
                pass
            
            try :
                lien = l.find_element(By .TAG_NAME, 'a')
                tab = va_chercher_img(lien.get_attribute('href'))
                for ligne in tab : 
                    txt = ligne[0] + "\t" + ligne[1]
                    txt = txt.replace("]]", "|120px]]\n")
                    file.write(nom+ " " +"style=\"text-align:center;\" | ")#ajout début de ligne
                    print(txt)
                    file.write(txt)
                file.write("\n\n\n")
            except : 
                pass


def va_chercher_img(lien) : 
    global LISTE_EXCEPTION
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path = "chromedriver.exe")
    driver.get(lien)
    try : 
        tab_class_img_wikimedia = driver.find_elements(By .CLASS_NAME, 'image')
        tab_lien_img_wikimedia = []
        i=0
        for img in tab_class_img_wikimedia : 
            l = img.get_attribute('href')
            if ((l in LISTE_EXCEPTION) or ('.svg' in l) or (i>=1)): 
                tab_class_img_wikimedia.remove(img)
            else :
                i+=1
                tab_lien_img_wikimedia.append((l, cherche_txt_inclusion(l)))

        return (tab_lien_img_wikimedia)
        
    except : 
        return (["pas d'img dommage\n"], [""])


        

def cherche_txt_inclusion(lien) : 
    #configuration du driver
    options = Options()
    options.headless = True #met l'execution en arrière plan
    driver = webdriver.Chrome(options=options, executable_path = "chromedriver.exe") 
    #on se deplace jusqu'au wikimedia de l'img passée en param
    driver.get(lien)
    sleep(2)

    try:
        liste_case = driver.find_elements(By .CLASS_NAME,'stockphoto_buttonrow')
        sleep(2)
        liste_case[2].click() #clique sur le lien "utiliser ce fichier"
        sleep(1)
        input_div = driver.find_elements(By .CLASS_NAME, 'stockphoto_dialog_row')
        print(input_div)
        input = input_div[1].find_element(By .TAG_NAME, 'input')
        txt = input.get_attribute('value')
        return (txt)
        
    except : 
        return("Euh ton prog marche ap\n")