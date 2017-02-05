# coding: utf-8
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import urllib.request
from os import path
import requests
import unicodedata
import re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(b'[^\w\s-]', b'', value).strip().lower()
    value = re.sub(b'[-\s]+', b'-', value)


# Changement de dossier de travail
os.chdir("C:/Users/Claude-Alban/Documents/Personnel/Projets/TikZParz")
# Récupération du contenu de la page
cont = requests.get("http://www.physagreg.fr/schemas-figures-physique-svg-tikz.php").text
# Affectation du chemin du résultat
chemin = u"./Résulat/"
# Affectation de la base de l'url de base
base_url = "http://www.physagreg.fr/"
# Sélection du HTML et remplissage de son contenu dans la variable éponyme

with open("newfile.txt","w") as f:
    f.write(cont)

with open("newfile.txt","r") as cont:
    soup = BeautifulSoup(cont,'html.parser')
    # Sélection des hearders, restriction des résultats aux six premiers et création des dossiers
    h5s = soup.find_all("h5",limit=6)
    for h5 in h5s:
        # Création des fichiers avec le nom des headers
        nom = str(slugify(h5.contents[0].string)).encode('utf8')
        os.makedirs(chemin + nom.decode('utf8'),exist_ok=True)
        # Sélection de la table soeur située juste après le header
        table = h5.find_next("table")
        # Sélection des headers contenant les titres des documents
        for h3 in table.select("h3"):
            # Création des répertoires avec les noms des figures
            titre = str(slugify(h3.text)).encode('utf8')
            os.makedirs(chemin + nom.decode('utf8') + '/' + titre.decode('utf8'),exist_ok=True)
            img = h3.find_next("img")
            src, title = img["src"], img["title"]
            # Encodage en utf-8 du titre de l'image
            title = str(slugify(title)).encode('utf8')
            # Joins la base et l'adresse associé à l'image
            img_url = urljoin(base_url, src)
            # Ouvre le fichier avec son titre comme nom
            with open(chemin + nom.decode('utf8') + '/' + titre.decode('utf8') + '/' + title.decode('utf8'), "w") as f:
                # Fais la requête de l'image sous forme de texte et l'écris dans le fichier
                f.write(requests.get(img_url).content.decode('utf8'))
            # Récupération du code TikZ située dans la balise soeur située juste après le header précédent
            code = img.find_next("p").text
            # Définition puis écriture du préambule et du code nécessaire à la production de l'image précédemment enregistrée
            preambule = r"%PREAMBULE \n\usepackage{pgfplots} \n\usepackage{tikz} \n\usepackage[european resistor, european voltage, european current]{circuitikz} \n\usetikzlibrary{arrows,shapes,positioning} \n\usetikzlibrary{decorations.markings,decorations.pathmorphing, decorations.pathreplacing} \n\usetikzlibrary{calc,patterns,shapes.geometric} \n%FIN PREAMBULE"
            with open(chemin + nom.decode('utf8') + '/' + titre.decode('utf8') + '/' + titre.decode('utf8') + u".tex",'w') as result:
                result.write(preambule + code)
