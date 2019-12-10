import requests
from pymongo import MongoClient
import pprint

<<<<<<< HEAD
def dowload_data_from_one_month(year, month):
=======

def download_data_from_one_month(year, month):
>>>>>>> refs/remotes/origin/master
    """
    This function makes a call the NYT archive API and pulls data from a given year and month and it returns a list of jsons containing the data.
    Params:
        - year: an int {1851, 1852, ... , 2018}
        - month: an int in {1, 2, 3, ... , 12}
    """
    response = requests.get(f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=EarvxAz31SAtamu5RGpqSfKOaT0Dhr59")
    json_response = response.json()
    docs = json_response['response']['docs']
    
    data = []

    for doc in docs:
        raw_date = doc['pub_date']
        doc['year'] = raw_date[0:4]

        month = raw_date[5:7]
        if month.startswith('0'):
            month = month.replace('0','')

        doc['month'] = month
        data.append(doc)

    return data


def download_and_insert_articles(db, year, month):
    """
    This function downloads and caches (saves in the database) a data from a given year and month.
    """
    data = download_data_from_one_month(year, month)
    db.articles.insert_many(data)


def get_articles_from_one_month(db, year, month):
    """
    This function returns a data from a given year and month. If the data is already in the database,
    it will not be downloaded again, and if it is not in the db, it will be downloaded and cached.
    """
    data = db.articles.find_one({'year': str(year)}, {'month': str(month)})
    if data is None:
        print("the data is not in the base")
        download_and_insert_articles(db, year, month)
        print("the data has been downloaded")
    
    
    output = []
    for article in db.articles.find({"$and":[ {"year": str(year)}, {"month": str(month)}] }):
        output.append(article)

    return output

def get_document_keywords_list(data):
    """
    Returns a list in the following format [[document_id_1, [key_words], ..., [document_id_n, [key_words]]]
    """
    output = []

    for doc in data:
        id = doc['_id']
        keywords = [keyword['value'] for keyword in doc['keywords']]
        output.append([id, keywords])

    return output

import collections
def get_word_to_count_dict(corpus):
    """
    Return a list in the following format: [{keyword: count}]
    """
    c = collections.Counter()
    for doc in corpus:
        keywords = doc[1]
        for keyword in keywords:
            c[keyword] += 1
    return [{key: c[key]} for key in c.keys()]

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.new_york_times

    #db.articles.drop()

    data = get_document_keywords_list(get_articles_from_one_month(db, 2010, 2))[1:100]

    print(get_word_to_count_dict(data))

