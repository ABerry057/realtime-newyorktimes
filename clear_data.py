"""
Utility script for clearing the database.
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")

    db = client.new_york_times

    db.articles.drop()