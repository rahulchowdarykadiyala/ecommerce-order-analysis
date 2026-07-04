import pandas as pd
import sqlite3

# connect to database
conn = sqlite3.connect("database/ecommerce.db")

# load CSV files
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv",sep=',')
#orders = pd.read_csv("data/orders.csv")

orders = pd.read_csv("data/orders.csv", sep=",")



# store in SQL
customers.to_sql("Customers", conn, if_exists="replace", index=False)
products.to_sql("Products", conn, if_exists="replace", index=False)
orders.to_sql("Orders", conn, if_exists="replace", index=False)


print(orders.head())
print(orders.columns)

print(products.head())
print(products.columns)

print(customers.head())
print(customers.columns)

print("Database created successfully!")

conn.close()