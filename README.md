# Using-ScienceDirect-API
Search and retrieve documents from ScienceDirect.

>"How do I search for documents I want to mine?"
>
>Elsevier's own search index for ScienceDirect can be targeted through:
>	"/content/search/scidir?query=[query]".
>	
>A request to this URL returns a list of documents matching the [query] with their basic metadata and their URIs to retrieve them from api.elsevier.com as well.
>
>(https://dev.elsevier.com/tecdoc_text_mining.html)

Two search processes will be done here. One to fetch all links and one to merge all articles from those links.
Through my tests, the Default APIKey only works when searching for individual articles, not when searching for [query].
To search for [query], I suggest you use the APIKEY available on the website through the Interactive API menu:
_https://dev.elsevier.com/sciencedirect.html#!/ScienceDirect_Search_V2/ScienceDirectSearchV2_
