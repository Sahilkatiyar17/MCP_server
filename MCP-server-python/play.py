d = {
  "searchParameters": {
    "q": "site:python.langchain.com/docs How to use Chromadb with langchain?",
    "type": "search",
    "engine": "google"
  },
  "organic": [
    {
      "title": "Spreedly | 🦜️🔗 LangChain",
      "link": "https://python.langchain.com/docs/integrations/document_loaders/spreedly/",
      "snippet": "This notebook covers how to load data from the Spreedly REST API into a format that can be ingested into LangChain, along with example usage for vectorization.See more",
      "position": 1
    },
    {
      "title": "OVHcloud",
      "link": "https://python.langchain.com/docs/integrations/text_embedding/ovhcloud/",
      "snippet": "This notebook explains how to use OVHCloudEmbeddings, which is included in the langchain_community package, to embed texts in langchain.See more",
      "position": 2
    }
  ],
  "credits": 1
} 

for a in d['organic']:
    print(a['link'])