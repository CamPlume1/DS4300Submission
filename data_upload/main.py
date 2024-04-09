# Importing libratries
from data_upload import data_load
from pymongo import MongoClient
import backend.api_methods.mongo_api as mongo_api

# Main script
def main():
    # Inserts OnlineRetail Data
    data_load.insert_online_retail_data()
    

if __name__ == '__main__':
    main()