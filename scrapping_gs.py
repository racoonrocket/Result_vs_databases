from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from time import sleep as sleep
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=object+detection+in+aerial+image+&btnG=&oq=ob'

response=requests.get(url,headers=headers)

def get_link(link_tag):

  links = []

  for i in range(len(link_tag)) :
    links.append(link_tag[i].a['href'])

  return links

def get_paperinfo(paper_url):

  #download the page
  response=requests.get(url,headers=headers)

  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    raise Exception('Failed to fetch web page ')

  #parse using beautiful soup
  paper_doc = BeautifulSoup(response.text,'html.parser')

  return paper_doc

def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})
  maxou = max([len(element) for element in [paper_tag,cite_tag,link_tag,author_tag]])
  return paper_tag,cite_tag,link_tag,author_tag,maxou


# it will return the title of the paper
def get_papertitle(paper_tag):
    paper_names = []

    for tag in paper_tag:
        paper_names.append(tag.select('h3')[0].get_text())

    return paper_names

# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  for i in cite_tag:
    cite = i.text
    print(cite)
    if i is None or cite is None:  # if paper has no citatation then consider 0
      cite_count.append(0)
    else:
      tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
      if tmp is None :
        cite_count.append(0)
      else :
        cite_count.append(int(tmp.group()))
  return cite_count


# function for the getting autho , year and publication information
def get_author_year_publi_info(authors_tag):
    years = []
    publication = []
    authors = []
    for i in range(len(authors_tag)):
        authortag_text = (authors_tag[i].text).split()
        try:
            year = int(re.search(r'\d+', authors_tag[i].text).group())
            years.append(year)
        except:
            years.append('no idea')

        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',', '', authortag_text[1])
        authors.append(author)

    return years, publication, authors

paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Citation' : [],
                    'Publication' : [],
                    'Url of paper' : [] }

# adding information in repository
def add_in_paper_repo(papername,year,author,cite,publi,link, maxouu):
  paper_repos_dict['Paper Title'].extend(papername)
  paper_repos_dict['Year'].extend(year)
  paper_repos_dict['Author'].extend(author)
  paper_repos_dict['Citation'].extend(cite)
  paper_repos_dict['Publication'].extend(publi)
  paper_repos_dict['Url of paper'].extend(link)
  print(paper_repos_dict)
  for element in paper_repos_dict:
      if len(paper_repos_dict[element]) < maxouu:
          paper_repos_dict[element] = ['not found'] * abs(maxouu-len(paper_repos_dict[element]))


  return pd.DataFrame(paper_repos_dict)


with open('USCS_corespondanceeeeeeee') as file:
    txt = file.read()
    txt = txt.split('\n')
    txt = [element.split(' ')[0] for element in txt]
    txt = txt[1:]

for element in txt:
    print(element)
    # get url for the each page
    url = "https://scholar.google.com/scholar?start={}&q=multiple+sclerosis+" + element

    # function for the get content of each page
    doc = get_paperinfo(url)

    # function for the collecting tags
    paper_tag, cite_tag, link_tag, author_tag, maxoo = get_tags(doc)
    print('paper_tag ' + str(len(paper_tag)) +   '    cite_tag ' + str(len(cite_tag)) + '       link_tag ' + str(len(link_tag)) + '    author_tag ' + str(len(author_tag)) + '     maxoo ' + str(maxoo))

    # paper title from each page
    papername = get_papertitle(paper_tag)

    # year , author , publication of the paper
    year, publication, author = get_author_year_publi_info(author_tag)

    # cite count of the paper
    cite = get_citecount(cite_tag)

    # url of the paper
    link = get_link(link_tag)

    # add in paper repo dict
    final = add_in_paper_repo(papername, year, author, cite, publication, link, maxoo)

    # use sleep to avoid status code 429
    sleep(100)

with open('google_scholar.csv','a+') as filecsv:
    final.to_csv(filecsv)