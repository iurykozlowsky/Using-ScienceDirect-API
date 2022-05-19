import json, requests

#SEARCH PARAMETERS:
_search = str(input("Search: ")).replace(" ","%20")
_count = int(input("\n\nNumber of articles (Max 200): "))
if _count > 200:
    exit()
key_query = str(input("APIKEY (Query): "))
key_content = str(input("APIKEY (Your Key): "))
output = open('output.json','w', encoding="utf8")
print("\nLoading...")


#QUERY SEARCH
url = "https://api.elsevier.com/content/search/sciencedirect?query=" + _search + "&count=" + str(_count) + "&apikey=" + key_query + ""

result = requests.get(url)
raw_data = json.loads(result.text)
article_count = len(raw_data['search-results']['entry']) #STORE ARTICLE COUNT INSIDE JSON AS 'LENGTH' FOR LOOPING


article_links = []
for item in range(article_count): #USE LOOPING FROM RANGE AS INDEX TO EACH JSON VALUE
#							                                \/
    article_links += {(raw_data['search-results']['entry'][item]['prism:url'])}
#							                                /\


xml_to_json = {'Accept': 'application/json'} #CONVERT INDIVIDUAL ARTICLE SEARCH RESULT FROM XML TO JSON
articles_json = {}
index = 1

for link in article_links:
    
    description = article["full-text-retrieval-response"]['coredata']['dc:description']
    
    if description is not None:
        description = description.strip()
    
    url_2 = link + "?apikey=" + key_content

    result2 = requests.get(url_2, headers=xml_to_json)

    article = json.loads(result2.text)

    articles_json[str(index)] = {

        "title" : article["full-text-retrieval-response"]['coredata']['dc:title'],
        "description" : description,
        "date" : article["full-text-retrieval-response"]['coredata']['prism:coverDisplayDate'],
        "link" : article["full-text-retrieval-response"]['coredata']['link'][-1]['@href']
    }

    index += 1


json.dump(articles_json, output, indent=4, ensure_ascii=False)
input("\ndone")
