import pandas as pd

# read dataframe from .csv file
df = pd.read_csv(r'BlackFriday.csv', encoding='ANSI')

# df.drop_duplicates(['User_ID', 'Product_ID'], 'first', True)

user = df[['User_ID', 'Gender', 'Age', 'City_Category', 'Stay_In_Current_City_Years', 'Marital_Status']]
product = df[['Product_ID', 'Product_Category_1', 'Product_Category_2', 'Product_Category_3']]
order = df[['User_ID', 'Product_ID', 'Occupation', 'Purchase']]

length = len(order) + 1
ids = range(1, length)
order_copy = order.copy()
order_copy['Purchase_ID'] = ids
order_copy.to_csv('order.csv', index=False, header=False)

user.to_csv('user.csv', index=False, header=False)
product.to_csv('product.csv', index=False, header=False)

# print(user.head())


