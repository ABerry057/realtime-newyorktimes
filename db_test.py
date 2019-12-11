import pytest
from get_data import *


def test_pull_one_month():
    data = download_data_from_one_month(1993, 1)
    assert len(data) == 6835


def test_download_and_insert():
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test_db
    db.articles.drop()
    
    download_and_insert_articles(db, 2007, 7)
    
    assert db.articles.count() == 11964


def test_caching():
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test_db
    db.articles.drop()
    
    year = 2009
    month = 3
    
    assert db.articles.find_one({"$and":[ {"year": str(2009)}, {"month": str(3)}] }) is None
    
    data = get_articles_from_one_month(db, year, month)
    
    assert len(data) == 13848
    assert db.articles.find_one({"$and":[ {"year": str(2009)}, {"month": str(3)}] }) is not None

    
def test_get_document_keywords_list():
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test_db
    db.articles.drop()
    
    year = 2009
    month = 3
    
    data = get_articles_from_one_month(db, year, month)
    
    list_of_pairs = get_document_keywords_list(data)
    assert len(list_of_pairs) == 13848
    
    # testing the format
    assert list_of_pairs[0][0] is not None
    assert list_of_pairs[0][1] is not None
    assert len(list_of_pairs[0]) == 2
    
    
def test_get_word_to_count_dict():
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test_db
    db.articles.drop()
    
    year = 2009
    month = 3
    
    data = get_articles_from_one_month(db, year, month)
    
    list_of_pairs = get_document_keywords_list(data)
    
    list_of_word_and_count_pairs = get_word_to_count_dict(list_of_pairs)
    
    assert len(list_of_word_and_count_pairs) == 7005
    assert len(list_of_word_and_count_pairs[0]) == 2
    
    

if __name__ == '__main__':
    
    
    # This will run all functions starting with `test_`
    pytest.main(['-v', __file__])