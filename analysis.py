import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("Analysis started...\n")

# Connect to database
conn = sqlite3.connect("database/ecommerce.db")

# Load tables
orders = pd.read_sql("SELECT * FROM Orders", conn)
customers = pd.read_sql("SELECT * FROM Customers", conn)
products = pd.read_sql("SELECT * FROM Products", conn)

print("Orders Data:")
print(orders)

# ================= SQL ANALYSIS =================

# Total Revenue
total_revenue = pd.read_sql("""
SELECT SUM(Quantity * Price) AS Revenue
FROM Orders
JOIN Products
ON Orders.ProductID = Products.ProductID
""", conn)

print("\nTotal Revenue:")
print(total_revenue)

# Top Products
top_products = pd.read_sql("""
SELECT ProductName, SUM(Quantity) AS TotalSold
FROM Orders
JOIN Products
ON Orders.ProductID = Products.ProductID
GROUP BY ProductName
ORDER BY TotalSold DESC
""", conn)

print("\nTop Selling Products:")
print(top_products)

# Revenue by City
city_revenue = pd.read_sql("""
SELECT City, SUM(Quantity * Price) AS Revenue
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID
JOIN Products
ON Orders.ProductID = Products.ProductID
GROUP BY City
""", conn)

print("\nRevenue by City:")
print(city_revenue)

# ================= NUMPY =================

print("\nNumPy Analysis:")
print("Average Quantity:", np.mean(orders["Quantity"]))
print("Max Quantity:", np.max(orders["Quantity"]))
print("Min Quantity:", np.min(orders["Quantity"]))
print("Standard Deviation:", np.std(orders["Quantity"]))

# ================= VISUALIZATION =================

# Top Products
plt.figure()
plt.bar(top_products["ProductName"], top_products["TotalSold"])
plt.title("Top Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.show()

# Revenue by City
plt.figure()
plt.bar(city_revenue["City"], city_revenue["Revenue"])
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.show()

# Payment Methods
payment = pd.read_sql("""
SELECT Payment, COUNT(*) as Count
FROM Orders
GROUP BY Payment
""", conn)

plt.figure()
plt.pie(payment["Count"], labels=payment["Payment"], autopct="%1.1f%%")
plt.title("Payment Methods")
plt.show()

# Monthly Trend
monthly = pd.read_sql("""
SELECT strftime('%Y-%m', OrderDate) AS Month,
SUM(Quantity * Price) AS Revenue
FROM Orders
JOIN Products
ON Orders.ProductID = Products.ProductID
GROUP BY Month
""", conn)

plt.figure()
plt.plot(monthly["Month"], monthly["Revenue"], marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

# ================= INSIGHTS =================

top_city = city_revenue.sort_values(by="Revenue", ascending=False).iloc[0]
top_product = top_products.iloc[0]

print("\nTop City:", top_city["City"])
print("Top Product:", top_product["ProductName"])

# Average Order Value
aov = total_revenue["Revenue"][0] / len(orders)
print("Average Order Value:", aov)

# Close DB
conn.close()