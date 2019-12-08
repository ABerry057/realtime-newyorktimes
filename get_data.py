import requests
from pymongo import MongoClient
import pprint


def dowload_data_from_one_month(year, month):
    response = requests.get(f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=EarvxAz31SAtamu5RGpqSfKOaT0Dhr59")
    json_response = response.json()
    docs = json_response['response']['docs']
    

    docs = docs[0:10]

    data = []

    for doc in docs:
        raw_date = doc['pub_date']
        doc['year'] = raw_date[0:4]
        doc['month'] = raw_date[5:7]
        data.append(doc)

    return data


def download_and_insert_articles(db, year, month):
    data = dowload_data_from_one_month(year, month)
    print(data)
    db.articles.insert_many(data)


def get_articles_from_one_month(db, year, month):
    data = db.articles.find_one({'year': str(year)}, {'month': str(month)})
    if data is None:
        print("the data is not in the base")
        download_and_insert_articles(db, year, month)
    
    
    output = []
    for article in db.articles.find({"$and":[ {"year": str(year)}, {"month": str(month)}] }):
        output.append(article)
        #{$and:[{"by":"tutorials point"},{"title": "MongoDB Overview"}]}
    

    return output


if __name__ == "__main__":
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.new_york_times

    #download_and_insert_articles(db, 2010, 1)

    #print(get_articles_from_one_month(db, 2011, 1)[5])

    #data = dowload_data_from_one_month(2010, 1)
    # insert_many_articles(db, data)

    db.articles.drop()

    #print(dowload_data_from_one_month(2010)[0])

    get_articles_from_one_month(db, 2010, '1')

