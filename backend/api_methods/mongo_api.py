# Importing libraries
from io import BytesIO

import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


# Extracts data via mongo and returns a dictionary where each month lists the total spending by country
def spending_by_month_and_country():

    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Cypher Query
    pipeline = [
        {"$project": {
            "Month": {"$month": "$InvoiceDate"},
            "Country": 1,
            "TotalAmount": {"$multiply": ["$Quantity", "$UnitPrice"]}
        }},
        {"$group": {
            "_id": {"Month": "$Month", "Country": "$Country"},
            "TotalAmount": {"$sum": "$TotalAmount"}
        }}
    ]

    # Runs cypher query
    results = collection.aggregate(pipeline)

    # Generates Result in dataframe
    data = pd.DataFrame(results)

    # Extract 'Month', 'Country', and 'TotalAmount' from '_id' field
    data[['Month', 'Country']] = pd.DataFrame(data['_id'].tolist())
    data.drop('_id', axis=1, inplace=True)
    months = data['Month'].tolist()
    countries = data['Country'].tolist()
    data['TotalAmount'] = data['TotalAmount'].round()
    total_amounts = data['TotalAmount'].tolist()

    # Create a dictionary to store total amount spent by country for each month
    month_data = {}
    for month, country, amount in zip(months, countries, total_amounts):
        if month not in month_data:
            month_data[month] = {}
        if country not in month_data[month]:
            month_data[month][country] = amount
        else:
            month_data[month][country] += amount

    # Sort month_data by month
    month_data = dict(sorted(month_data.items()))

    # Changes month from number to the month's actual name
    month_sales = {}
    month_sales['January'] = month_data.get(1)
    month_sales['February'] = month_data.get(2)
    month_sales['March'] = month_data.get(3)
    month_sales['April'] = month_data.get(4)
    month_sales['May'] = month_data.get(5)
    month_sales['June'] = month_data.get(6)
    month_sales['July'] = month_data.get(7)
    month_sales['August'] = month_data.get(8)
    month_sales['September'] = month_data.get(9)
    month_sales['October'] = month_data.get(10)
    month_sales['November'] = month_data.get(11)
    month_sales['December'] = month_data.get(12)

    client.close()

    return month_sales


# Given the selected countires, vizualizes their spending by month
def plot_country_spending(specified_countries):

    # Gets cypher queried data as a dictionary and coverst to a data frame
    data = spending_by_month_and_country()
    df = pd.DataFrame(data).T

    # Vizualization
    plt.figure(figsize=(6, 4))

    # Plot data for each country that is apart of the specified list
    for country in specified_countries:
        if country in df.columns:
            plt.plot(df.index, df[country], label=country)

    # Add labels, title, and legend
    plt.xlabel('Month')
    plt.ylabel('Amount Spent')
    plt.title('Amount Spent by Country per Month')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()

    return figfile

def get_unique_countries() -> list[str]:
    '''
    Gets the unique countries
    :return:
    '''
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    unique_countries = collection.distinct('Country')
    client.close()
    return unique_countries

def get_data(Country):
       # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$match': {
            'Country': Country,
            '$expr': { '$eq': [{ '$year': "$InvoiceDate" }, 2011] }
            }
        },
        {
            '$project': {
            'month': { '$month': "$InvoiceDate" },
            'revenue': { '$multiply': ["$UnitPrice", "$Quantity"] }
            }
        },
        {
            '$group': {
            '_id': "$month" ,
            'totalRevenue': { '$sum': "$revenue" }
            }
        },
        {
            '$sort': { "_id": 1 }
        }
        ]

    # Query the dataset
    result = list(collection.aggregate(pipeline))


    result = pd.DataFrame(result)
    result['Month'] = result['_id'].apply(number_to_month)
    return result



def number_to_month(number):
    months = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    return months[number - 1]


def linear_regression(X,y):
    model = LinearRegression()
    model.fit(X.reshape(-1,1), y)
    predictions = model.predict(X)

    return predictions


def gen_country_graphic(Country) -> BytesIO:

    data = get_data(Country)


    if data.empty:
        return "Country Not Found"
    else:
        plt.figure(figsize=(6, 4))
        plt.bar(data['Month'], data['totalRevenue'], width=.8)
        # Add labels and title
        plt.xlabel('Month', fontsize=12)  # Adjust font size
        plt.ylabel('Amount Spent', fontsize=12)  # Adjust font size
        plt.title('Amount Spent in ' + Country + ' (2011)', fontsize=14)  # Adjust font size
        # Rotate x-axis labels if needed
        plt.xticks(rotation=70)  # Rotate labels by 45 degrees
        def format_func(value, tick_number):
            return f'{value/1:.0f}'
        # Set the custom formatter for y-axis tick labels
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
        # Display the plot
        plt.tight_layout()

        if data.shape[0] > 1:
            x = np.array(data.index.values.reshape(-1,1))
            y = linear_regression(x, data['totalRevenue'].values)
            plt.plot(data.index.values, y, linestyle='dashed', color='blue', linewidth=2.5)




        # Save the plot to a BytesIO object
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # Move the cursor to the beginning of the BytesIO object
        plt.clf()
        plt.close()

        return figfile



def best_selling_products(year) -> BytesIO:
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Query
    pipeline = [
        {
            '$match': {
                '$expr': {'$eq': [{'$year': "$InvoiceDate"}, year]}
            }
        },
        {
            '$project': {
                'Description': 1,
                'Quantity': 1
            }
        },
        {
            '$group': {
                '_id': "$Description",
                'TotalQuantity': {'$sum': "$Quantity"}
            }
        },
        {
            '$sort': {"TotalQuantity": -1}
        },
        {
            '$limit': 10
        }
    ]
    # Run query
    results = collection.aggregate(pipeline)

    # Store Result
    data = pd.DataFrame(results)

    # Plot results
    fig, ax = plt.subplots(figsize=(6, 4))

    # Plot the results part II
    ax.bar(data['_id'], data['TotalQuantity'])

    # Add labels and title
    ax.set_xlabel('Product Description')
    ax.set_ylabel('Total Quantity Sold')
    ax.set_title('Top 10 Best Selling Products by Year, (' + str(year) + ')')

    # Rotate x-axis to look fancy
    # plt.xticks(rotation=70)

    plt.xticks(data['_id'], rotation=90)
    for i, v in enumerate(data['TotalQuantity']):
        ax.text(i, v, str(v), color='black', ha='center')

    # Save the plot
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()

    return figfile


def get_time_series_data():
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']
    pipeline = [
        {
            '$project': {
                'YearMonth': {
                    '$dateToString': {'format': "%Y-%m", 'date': "$InvoiceDate"}
                },
                'Quantity': "$Quantity"
            }
        },
        {
            '$group': {
                '_id': "$YearMonth",
                'TotalQuantity': {'$sum': "$Quantity"}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]

    result = list(collection.aggregate(pipeline))
    client.close()

    # Transform the result into a pandas DataFrame
    result_df = pd.DataFrame(result)
    result_df['YearMonth'] = pd.to_datetime(result_df['_id'])
    result_df.drop('_id', axis=1, inplace=True)
    result_df.sort_values('YearMonth', inplace=True)
    return result_df


# Andrews Graphic
def gen_time_series_graphic() -> BytesIO:
    data = get_time_series_data()

    # Plot the time series data
    plt.figure(figsize=(6, 4))
    plt.plot(data['YearMonth'], data['TotalQuantity'], marker='o')

    # Adding plot title and labels
    plt.title('Monthly Quantity Sold Over All Years')
    plt.xlabel('Year-Month')
    plt.ylabel('Total Quantity')
    plt.grid(True)
    plt.xticks(rotation=90)

    # Improve the x-axis representation
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=6))
    plt.gcf().autofmt_xdate()  # Beautify the x-labels

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()
    return figfile

def spending_by_month_and_country():

    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['OnlineRetail']
    collection = db['OnlineRetail']

    # Cypher Query
    pipeline = [
        {"$project": {
            "Month": {"$month": "$InvoiceDate"},
            "Country": 1,
            "TotalAmount": {"$multiply": ["$Quantity", "$UnitPrice"]}
        }},
        {"$group": {
            "_id": {"Month": "$Month", "Country": "$Country"},
            "TotalAmount": {"$sum": "$TotalAmount"}
        }}
    ]

    # Runs cypher query
    results = collection.aggregate(pipeline)

    # Generates Result in dataframe
    data = pd.DataFrame(results)

    # Extract 'Month', 'Country', and 'TotalAmount' from '_id' field
    data[['Month', 'Country']] = pd.DataFrame(data['_id'].tolist())
    data.drop('_id', axis=1, inplace=True)
    months = data['Month'].tolist()
    countries = data['Country'].tolist()
    data['TotalAmount'] = data['TotalAmount'].round()
    total_amounts = data['TotalAmount'].tolist()

    # Create a dictionary to store total amount spent by country for each month
    month_data = {}
    for month, country, amount in zip(months, countries, total_amounts):
        if month not in month_data:
            month_data[month] = {}
        if country not in month_data[month]:
            month_data[month][country] = amount
        else:
            month_data[month][country] += amount

    # Sort month_data by month
    month_data = dict(sorted(month_data.items()))

    # Changes month from number to the month's actual name
    month_sales = {}
    month_sales['January'] = month_data.get(1)
    month_sales['February'] = month_data.get(2)
    month_sales['March'] = month_data.get(3)
    month_sales['April'] = month_data.get(4)
    month_sales['May'] = month_data.get(5)
    month_sales['June'] = month_data.get(6)
    month_sales['July'] = month_data.get(7)
    month_sales['August'] = month_data.get(8)
    month_sales['September'] = month_data.get(9)
    month_sales['October'] = month_data.get(10)
    month_sales['November'] = month_data.get(11)
    month_sales['December'] = month_data.get(12)

    return month_sales

# Given the selected countires, vizualizes their spending by month
def plot_country_spending(specified_countries):
    # Gets cypher queried data as a dictionary and coverst to a data frame
    data = spending_by_month_and_country()
    df = pd.DataFrame(data).T

    # Vizualization
    plt.figure(figsize=(6, 4))

    # Plot data for each country that is apart of the specified list
    for country in specified_countries:
        if country in df.columns:
            plt.plot(df.index, df[country], label=country)

    # Add labels, title, and legend
    plt.xlabel('Month')
    plt.ylabel('Amount Spent')
    plt.title('Amount Spent by Country per Month')
    plt.legend()

    # Show plot
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    plt.close()
    return figfile

