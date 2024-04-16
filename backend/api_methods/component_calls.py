from io import BytesIO

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt


# Created by Cam Plume

# creates vis for customer sales profiles
def cam_viz(product_array) -> BytesIO:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    operator = "$in"
    if len(product_array) == 0:
        operator = "$nin"
    # set up pipeline
    pipeline = [
        {"$match": {"Description": {operator: product_array}}},
        {"$group":
             {"_id": "$CustomerID",
              "total_spending": {"$sum": {"$multiply": ["$Quantity", "$UnitPrice"]}},
              "occurrences": {"$sum": 1},
              "Description": {"$addToSet": "$Description"}}
         }
    ]
    # Run query and load results to a dataframe
    cursor = collection.aggregate(pipeline)
    df = pd.DataFrame(cursor)

    # Data Cleaning Remove outlier-> Good for demo, bad for product
    # df.drop(df['total_spending'].idxmax(), inplace=True)

    # Given query, create scatterplot
    plt.figure(figsize=(6, 4))

    # If product_array length is greater than 0, encode Description as color
    if len(product_array) > 1:
        plt.scatter(df['occurrences'], df['total_spending'],  c=df['Description'].apply(lambda x: hash(tuple(x))))
    else:
        plt.scatter(df['occurrences'], df['total_spending'])

    # Labeling
    plt.title('Unique Customer Profiles: Transactions vs Total Spending')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Total Spending, in British Pounds Sterling')

    # Fix y-axis [0, max + 10% max]
    plt.ylim(0, max(df['total_spending'] + 0.1 * max(df['total_spending'])))

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()
    return figfile


# Legacy test method from API dev
def cam_test(test_str: str) -> str:
    return test_str + " returned"

# Gets the unique countries from our dataset
def countries() -> list[str]:
    '''
    Gets the unique countries
    :return: list of str
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    unique_countries = collection.distinct('Country')
    client.close()
    return unique_countries

# Gets unique products from dataset
def unique_descriptions() -> list[str]:
    '''
    Gets the unique product descriptions
    :return: list of str
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    unique_description = collection.distinct('Description')
    unique_lowered = [str(x).lower() for x in unique_description]
    client.close()
    return unique_lowered


# gets unique years from the dataset
def years() -> list[str]:
    '''
    Gets the unique years from the dataset
    :return: list of years in string format
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    unique_dates = collection.distinct('InvoiceDate')
    unique_years = [date.year for date in unique_dates]
    client.close()
    return list(set(unique_years))


def total_transactions() -> int:
    '''
    Gets the total number of transactions in a dataset
    :return: int
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    total_count = collection.count_documents({})
    client.close()
    return total_count


# Gets total number of transactions
def total_sales() -> int:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    total_sales = 0

    pipeline = [
        {
            '$project': {
                'transaction_total': {'$multiply': ['$UnitPrice', '$Quantity']}
            }
        },
        {
            '$group': {
                '_id': None,
                'total_sales': {'$sum': '$transaction_total'}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))
    sales_total = result[0]['total_sales']
    client.close()
    return sales_total

# Gets total units sold
def total_units() -> int:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    total_sales = 0

    pipeline = [
        {
            '$group': {
                '_id': None,
                'total_sales': {'$sum': '$Quantity'}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))
    sales_total = result[0]['total_sales']
    client.close()
    return sales_total

# Gets most frequent unit sold
def top_unit() -> str:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$group': {
                '_id': '$Description',
                'total_quantity': {'$sum': '$Quantity'}}
        },
        {
            '$sort': {'total_quantity': -1}},
        {
            '$limit': 1}
    ]
    result = list(collection.aggregate(pipeline))
    top_description = result[0]['_id']
    client.close()
    return top_description

# Gets top unit by revenue
def top_unit_rev() -> str:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$group': {
                '_id': '$Description',
                'total_sales': {'$sum': {'$multiply': ['$UnitPrice', '$Quantity']}}
            }
        },
        {
            '$sort': {'total_sales': -1}
        },
        {
            '$limit': 1
        }
    ]
    result = list(collection.aggregate(pipeline))
    top_description = result[0]['_id']
    client.close()
    return top_description

# Gets top country by quantity sold
def top_country() -> str:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$group': {
                '_id': '$Country',
                'total_quantity': {'$sum': '$Quantity'}}
        },
        {
            '$sort': {'total_quantity': -1}},
        {
            '$limit': 1}
    ]
    result = list(collection.aggregate(pipeline))
    top_country = result[0]['_id']
    client.close()
    return top_country
