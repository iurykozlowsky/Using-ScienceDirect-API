import json, requests

'''
===================================================================================================================================================

"How do I search for documents I want to mine?"
Elsevier's own search index for ScienceDirect can be targeted through:

	https://api.elsevier.com/content/search/scidir?query=[query].

A request to this URL returns a list of documents matching the [query] with their basic metadata and their URIs to retrieve them from api.elsevier.com as well.
(https://dev.elsevier.com/tecdoc_text_mining.html)

===================================================================================================================================================

Dois processos de busca serão feitos aqui. Um para buscar todos os links, e outro para buscar todos os artigos a partir desses links. E também, duas
APIKeys diferentes serão usadas, porque só é possível usar a APIKEY default na busca por artigos individuais, e não na primeira busca por [query].
Para busca por [query], sugiro que use a APIKEY que o site disponibiliza através do menu de API Interativa:
https://dev.elsevier.com/sciencedirect.html#!/ScienceDirect_Search_V2/ScienceDirectSearchV2

==================================================================================================================================================='''


#PARÂMETROS DE PESQUISA:
busca = str(input("Termo de busca: "))
quantidade = int(input("\n\nQuantidade de artigos (Max 200): ")) #MÁXIMO 200
if quantidade > 200:
    exit()
chave_query = str(input("APIKEY (Query): "))
chave_content = str(input("APIKEY (Your Key): "))
output = open('output.json','w', encoding="utf8")


#URL DE BUSCAS DE TODOS OS LINKS DOS ARTIGOS QUE CONTÉM O TERMO BUSCADO
url = "https://api.elsevier.com/content/search/sciencedirect?query=" + busca + "&count=" + str(quantidade) + "&apikey=" + chave_query + ""

resultado = requests.get(url) #RETORNA UM OBJETO 'RESPONSE' COM O METODO GET
dados_brutos = json.loads(resultado.text) #CARREGA O TEXTO DO RESPONSE COMO JSON EM UM OBJETO PYTHON
quantidade_artigos = len(dados_brutos['search-results']['entry']) #SALVA A QUANTIDADE DE RESULTADOS DENTRO DO JSON COMO LENGHT PARA O LOOPING



links_dos_artigos = []
for item in range(quantidade_artigos): #USA O LOOPING DO RANGE COMO INDEX PARA CADA ITEM DO JSON 'DADOS BRUTOS'

    links_dos_artigos += {(dados_brutos['search-results']['entry'][item]['prism:url'])}



xml_to_json = {'Accept': 'application/json'} #CONVERTE O RESULTADO DA BUSCA INDIVIDUAL DE ARTIGOS DE XML PARA JSON
artigos_json = {} #DICT EXTERNO
index = 1

for link in links_dos_artigos:
    
    url_2 = link + "?apikey=" + chave_content

    resultado2 = requests.get(url_2, headers=xml_to_json) #RETORNA UM OBJETO 'RESPONSE' COM O METODO GET, E USA 

    artigo = json.loads(resultado2.text) #CARREGA O TEXTO DO RESPONSE COMO JSON EM UM OBJETO PYTHON

    artigos_json[str(index)] = { #SALVA DADOS EM DICTS INTERNOS DIFERENTES A PARTIR DO INDEX

        "titulo" : artigo["full-text-retrieval-response"]['coredata']['dc:title'],
        "resumo" : artigo["full-text-retrieval-response"]['coredata']['dc:description'].strip(),
        "data" : artigo["full-text-retrieval-response"]['coredata']['prism:coverDisplayDate'],
        "link" : artigo["full-text-retrieval-response"]['coredata']['link'][-1]['@href']
    }

    index += 1


json.dump(artigos_json, output, indent=4, ensure_ascii=False)
print("\ndone")