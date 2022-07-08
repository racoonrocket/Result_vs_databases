import requests
import json
import re
import time

def clean_html_msgene():
    with open("MSGENE DATABASE") as msgene:
        texte = msgene.read()
        liste= texte.split("\n")
        retour = ''
        print(liste)
        for element in liste:
            print(element)
            m = re.search('[>]([A-Z,1-9]*)[<]', element)
            if m != None:
                 print(m.group(1))
                 retour += m.group(1) + "\n"
        with open("MSGENE_datatbase_clean","w+") as msgeneclean:
            msgeneclean.write(retour)

def transform_region():
    with open("MTHRregion") as region:
        texte = region.read()
        liste = texte.split("\n")
        new_liste = []
        for element in liste:
            m = re.search('chr([0-9]*)_', element)
            if m != None:
                new_liste.append(m.group(1) + ":" + element.split(" ")[0].split("\t")[1] + "-" + element.split(" ")[0].split("\t")[2])
        print(new_liste)
    return new_liste


def run_the_search():
    for element in transform_region():
        genes = get_loci_from_gene(name = element)
        if len(genes) > 1 :
            result = compared_loci(genes)
        if genes == []:
            with open('similar_gnees', 'a+') as similar_genes:
                similar_genes.write(element + "   " + "NO RESULT FOR THE REGION \n")
        else:
            with open('similar_gnees','a+') as similar_genes:
                similar_genes.write(element + "   " + result + "\n")

def get_loci_from_gene(name = "1:11883736-11900280"):
    #https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search' -i -H 'Accept: application/json'
    api_url = "https://www.ebi.ac.uk/gwas/rest/api/snpLocation/" + name
    response = requests.get(api_url)
    print(type(response))
    response = response.json()
    print(type(response))
    yep = get_recursively(response,'geneName')
    print(yep)
    time.sleep(2)
    return yep

def compared_loci(loci_liste):
    found_same = []
    # with open('geneMSA') as geneMSA:
    #     txt_geneMSA = geneMSA.read()
    #     txt_geneMSA = txt_geneMSA.replace(" ","\n")
    #     liste_geneMSA = txt_geneMSA.split("\n")
    # with open('IMSGC') as IMSGC:
    #     txt_IMSGC = IMSGC.read()
    #     txt_IMSGC = txt_IMSGC.replace(" ","\n")
    #     liste_IMSGC = txt_IMSGC.split("\n")
    liste_IMSGC, liste_geneMSA = [],[]
    with open('MSGENE DATABASE') as MSGENE:
        txt_MSGENE = MSGENE.read()
        txt_MSGENE = txt_MSGENE.replace(" ","\n")
        liste_MSGENE = txt_MSGENE.split("\n")
    for element in loci_liste:
        if element in liste_IMSGC or element in liste_geneMSA or element in liste_MSGENE:
            print(element)
            found_same.append(element)
    return(element)

def dumb_compared():
    # with open('geneMSA') as geneMSA:
    #     txt_geneMSA = geneMSA.read()
    #     txt_geneMSA = txt_geneMSA.replace(" ","\n")
    #     liste_geneMSA = txt_geneMSA.split("\n")
    #     print(liste_geneMSA)
    # with open('IMSGC') as IMSGC:
    #     txt_IMSGC = IMSGC.read()
    #     txt_IMSGC = txt_IMSGC.replace(" ","\n")
    #     liste_IMSGC = txt_IMSGC.split("\n")
    #     print(liste_IMSGC)
    with open('MSGENE_datatbase_clean') as MSGENE:
        txt_MSGENE = MSGENE.read()
        txt_MSGENE = txt_MSGENE.replace(" ","\n")
        liste_MSGENE = txt_MSGENE.split("\n")
        print(liste_MSGENE)
    with open('MTHRloci') as MTHRloci:
        txt_MTHRloci = MTHRloci.read()
        liste_MTHRloci = txt_MTHRloci.split("\n")
        print(liste_MTHRloci)
    for element in liste_MTHRloci:
        if element in liste_MSGENE:
            print(element)
