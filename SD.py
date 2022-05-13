import json, requests

'''
==================================================================================================================================================================

"How do I search for documents I want to mine?"
Elsevier's own search index for ScienceDirect can be targeted through:

	https://api.elsevier.com/content/search/scidir?query=[query].

A request to this URL returns a list of documents matching the [query] with their basic metadata and their URIs to retrieve them from api.elsevier.com as well.
(https://dev.elsevier.com/tecdoc_text_mining.html)

==================================================================================================================================================================

Two search processes will be done here. One to fetch all links and one to merge all articles from those links.
Through my tests, the Default APIKey only works when searching for individual articles, not when searching for [query].
To search for [query], I suggest you use the APIKEY available on the website through the Interactive API menu:
https://dev.elsevier.com/sciencedirect.html#!/ScienceDirect_Search_V2/ScienceDirectSearchV2

=================================================================================================================================================================='''


#SEARCH PARAMETERS:
_search = str(input("Search: "))
_count = int(input("\n\nNumber of articles (Max 200): "))
if _count > 200:
    exit()
key_query = str(input("APIKEY (Query): "))
key_content = str(input("APIKEY (Your Key): "))
output = open('output.json','w', encoding="utf8")


#QUERY SEARCH
url = "https://api.elsevier.com/content/search/sciencedirect?query=" + _search + "&count=" + str(_count) + "&apikey=" + key_query + ""

result = requests.get(url)
raw_data = json.loads(result.text)
article_count = len(raw_data['search-results']['entry']) #STORE ARTICLE COUNT INSIDE JSON AS 'LENGTH' FOR LOOPING



article_links = []
for item in range(article_count): #USE LOOPING FROM RANGE AS INDEX TO EACH JSON VALUE

    article_links += {(raw_data['search-results']['entry'][item]['prism:url'])}



xml_to_json = {'Accept': 'application/json'} #CONVERT INDIVIDUAL ARTICLE SEARCH RESULT FROM XML TO JSON
articles_json = {}
index = 1

for link in article_links:
    
    url_2 = link + "?apikey=" + key_content

    result2 = requests.get(url_2, headers=xml_to_json)

    article = json.loads(result2.text)

    articles_json[str(index)] = {

        "title" : article["full-text-retrieval-response"]['coredata']['dc:title'],
        "description" : article["full-text-retrieval-response"]['coredata']['dc:description'].strip(),
        "date" : article["full-text-retrieval-response"]['coredata']['prism:coverDisplayDate'],
        "link" : article["full-text-retrieval-response"]['coredata']['link'][-1]['@href']
    }

    index += 1


json.dump(articles_json, output, indent=4, ensure_ascii=False)
print("\ndone")
