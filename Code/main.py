# coding: utf-8
import os
import re
from bs4 import BeautifulSoup as bs

os.chdir("C:/Users/Claude-Alban/Documents/Personnel/Projets/ProjectTikz")
# Sélection du HTML et remplissage de son contenu dans la variable éponyme
with open("C:/Users/Claude-Alban/Documents/Personnel/Projets/ProjectTikz/Nouvelle tentative/Donnees/Physagreg.htm","r") as html:
    html = bs(html,'html.parser')
    # Sélection des hearders, restriction des résultats aux six premiers et création des dossiers
    h5 = html.find_all("h5",limit=6)
    for h in h5:
        # Création des fichiers avec le nom des headers
        chemin = u"./Résulat/"
        nom = str(h.contents[0].string).encode('utf8')
        os.makedirs(chemin + nom.decode('utf8'),exist_ok=True)
        # Sélection de la table soeur située juste après le header
        table = h.find_next_siblings(name = 'table')
        for t in table:
            # Sélection des headers contenant les titres des documents
            h3 = t.find_all("h3")
            for k in h3:
                titre = str(k.string).encode('utf8')
                # Création des répertoires avec les noms des figures
                os.makedirs(chemin + nom.decode('utf8') + titre.decode('utf8'),exist_ok=True)
                # Récupération de l'image située dans la balise soeur située juste après le header précédent
                img = k.find_next_sibling("img")
                chimg = img.img['src']
                os.fdopen(img.img['title'])
                # Récupération du code TikZ située dans la balise soeur située juste après le header précédent
                tikz = k.find_next_sibling('p')
                # Extraction du code TikZ contenu dans la balise précédemment récupérée
                code = tikz.get_text()
                # Définition puis écriture du préambule et du code nécessaire à la production de l'image précédemment enregistrée
                preambule = r"%PREAMBULE \n  \usepackage{pgfplots} \n  \usepackage{tikz} \n  \usepackage[european resistor, european voltage, european current]{circuitikz} \n  \usetikzlibrary{arrows,shapes,positioning} \n  \usetikzlibrary{decorations.markings,decorations.pathmorphing, decorations.pathreplacing} \n  \usetikzlibrary{calc,patterns,shapes.geometric} \n  %FIN PREAMBULE"
                with open(chemin + nom + titre + ".tex",'w') as result:
                    result.write(preambule + code)
