import requests
import json
import re
import time


def compared_loci2(element):
    """

    :param element:
    :return: element if in MSDATA BASE or str if not in
    """
    found_same = []
    liste_IMSGC, liste_geneMSA = [],[]
    with open('MSGENE DATABASE') as MSGENE:
        txt_MSGENE = MSGENE.read()
        txt_MSGENE = txt_MSGENE.replace(" ","\n")
        liste_MSGENE = txt_MSGENE.split("\n")

    if element in liste_IMSGC or element in liste_geneMSA or element in liste_MSGENE:
        print(element)
        found_same.append(element)
        return(element)
    else:
        return ' NOT IN MS DATABASE '


def transform_region2():
    """
    Parsing of txt file from ctrl +c of a csv (to be deleted)
    :return:
    """
    with open("MTHRregionbis") as region:
        texte = region.read()
        liste = texte.split("\n")
        new_liste = []
        for element in liste:
            ya = element.split('\t')
            if len(ya) > 1 :
                new_liste.append([ya[0],ya[1]])
        print(new_liste[1:])
    return new_liste[1:]



def get_loci_from_gene2(name = "1:11883736-11900280"):
    """
    Call UCSC API (knowGene track)
    :param name: region of the genome with chr:pos
    :return:uc ID of the gene corresponding to the input region and str 'non codant' if no gene found in ucsc
    """
    print('NAAAME')
    print(name)
    #https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search' -i -H 'Accept: application/json'
    #api_url = "api.genome.ucsc.edu/getData/track?genome=hg38;track=gold;chrom=chr1;start=47000;end=48000" + name
    api_url = "https://api.genome.ucsc.edu/getData/track?genome=hg19;maxItemsOutput=5;track=knownGene;chrom=" + (name[0]) + ";start=" + str(int(name[1])-1) +";end=" + name[1]
#kgXref

    response = requests.get(api_url)
    response = response.json()
    yep = get_recursively(response,'name')
    print('different plqces' + str(yep))
    with open("kgXref.txt") as ref:
        openedref = ref.read()
        openedref = openedref.split("\n")
        openedref = [openedref[k].split("\t") for k in range(len(openedref))]
    try:
        with open("USCS_corespondanceeeeeeee", 'a+') as ucsccores:
            ucsccores.write('\n')
        for x in yep:
            for element in openedref:
                if x in element:
                    with open("USCS_corespondanceeeeeeee", 'a+') as ucsccores:
                        ucsccores.write(element[4] + ' ')
        return 'non codant'
    except:
        return 'non codant'



def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found



def run_the_search2():
    """
    Litle pipeline to compared ignacio genes to some database genes (to be transformed to main)
    :return:
    """
    liste_genes = []
    for element in transform_region2():
        genes = get_loci_from_gene2(name = element)
        print(genes,"YO¨POYJROKN")
        if genes != 'non codant':
            result = compared_loci2(genes)
        if genes == 'non codant':
            with open('similar_gnees', 'a+') as similar_genes:
                similar_genes.write(element[0] + ":" + element[1] + " "  + genes +" " + "non codant \n")

        else:
            with open('similar_gnees','a+') as similar_genes:
                similar_genes.write(element[0] + ":" + element[1] + " " +genes +" " + result + "\n")
        liste_genes.append(genes)
    return liste_genes


def call_ncbi_vs_mthrgenes():
    import xmltodict
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&query_key=1&WebEnv=MCID_62c6fdb8d536a754607ea718"
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    liste = get_recursively(data, 'Name')
    print(len(liste))

    with open('MTHRregiostierce') as nome:
        red_nome = nome.read()
        red_nome = red_nome.split('\n')
        print(red_nome)
    for element in liste:
        if element in red_nome:
            print(element)


################################################SCRIPT######################################################################du
run_the_search2()