from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

"""Web scrapping and Automation"""


path = "C:/driver/chromedriver-win64/chromedriver/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

try:

    driver.maximize_window()
    driver.get('https://google.com')
  
    search = driver.find_element(By.ID,"APjFqb").send_keys('Github.com')
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'btnK'))).click()

    git_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'github'))).click()
    
    git_box = driver.find_element(by='xpath', value='/html/body/div[1]/div[1]/header/div/div[2]/div/div/qbsearch-input/div[1]/button/span').click()

    git_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'query-builder-test')))
    
    git_search.send_keys('Pandas-Data-Science-Tasks')
    time.sleep(1)
    
    git_search.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'KeithGalli'))).click()
    time.sleep(2)
    
    driver.find_element(by='xpath',value='//*[@id="repo-content-pjax-container"]/div/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[3]/div[2]/span/a').click()
    time.sleep(1)
    
    driver.find_element(by='xpath',value='//*[@id="folder-row-2"]/td[2]/div/div/h3/div/a').click()
    time.sleep(2)


    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for month in months:

        file = pd.read_csv(f"https://raw.githubusercontent.com/KeithGalli/Pandas-Data-Science-Tasks/master/SalesAnalysis/Sales_Data/Sales_{month}_2019.csv")

        df = pd.DataFrame(file)
        loc = "C:/Users/U6074525/OneDrive - Clarivate Analytics/Desktop/project_september/sales_project/download/"
        filename = f'{loc}{month}.csv'
        df.to_csv(filename,index=False)

except Exception as e:
    print(f"An error occurred: {str(e)}")

driver.quit()


"""Merging the Each months data"""


path="C:/Users/U6074525/OneDrive - Clarivate Analytics/Desktop/project_september/sales_project/download/"

files = [file for file in os.listdir(path) if not file.startswith('.')] # Ignore hidden files

all_months_data = pd.DataFrame()

for file in files:
    current_data = pd.read_csv(path+"/"+file)
    all_months_data = pd.concat([all_months_data, current_data])

all_months_data.to_csv("single_file.csv", index=False)
all_data = pd.read_csv("single_file.csv")
print(all_data.head())


"""Cleaning The Data"""


nan_df = all_data[all_data.isna().any(axis=1)]
print(nan_df.head())

all_data = all_data.dropna(how='all')
print(all_data.head())
 
all_data = all_data[all_data['Order Date'].str[0:2]!='Or']

 
"""Correcting the column """


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# Adding the months Column

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
print(all_data.head())

all_data['Month 2'] = pd.to_datetime(all_data['Order Date']).dt.month
print(all_data.head())
 

# Adding the City Column

 
def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
print(all_data.head())


"""Sorting the Data"""


all_data.sort_values(["Order Date"],axis=0,ascending=[False],inplace=True)

all_data.sort_values(["Product", "Order Date", "Month"],axis=0,ascending=[True, True, True],inplace=True)

print(all_data.head())


""" 1. Finding the best Month"""


all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')

print(all_data.groupby(['Month']).sum())
 
# Bar Graph

months = range(1,13)
print(months)

monthly_sales = all_data.groupby('Month')['Sales'].sum().reset_index()

monthly_sales.to_csv('monthly_sales.csv', index=False)

plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()

 
""" 2. Which city sold the most product"""

res=all_data.groupby(['City']).sum()
print(res)

# Plotting
 
max_sales_city = res['Sales'].idxmax()
max_sales_value = res['Sales'].max()


cities=res.index
sales = res['Sales']

sales_data = pd.DataFrame({'City': cities, 'Sales': sales})

sales_data.to_csv('sales_by_city.csv', index=False)
print(sales)

plt.bar(cities,sales)
plt.xticks(cities,rotation = 'vertical', size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.show()

print(f"Most products are sold in: {max_sales_city} \nSales is: {max_sales_value}")


""" 3. Best Time to Display Advertisement"""


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute

 
all_data['Count'] = 1
print(all_data.head())

hours = [hour for hour, df in all_data.groupby('Hour')]

hourly_counts = all_data.groupby('Hour')['Count'].count().reset_index()

# Save the hourly counts to a CSV file
hourly_counts.to_csv('hourly_counts.csv', index=False)

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()


""" 4. products that are sold most often"""


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df = df[['Order ID','Grouped']].drop_duplicates()

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))

for key,value in count.most_common(10):
    print(key,value)


product_group = all_data.groupby('Product')
quantity_ordered = product_group['Quantity Ordered'].sum()
products = [product for product,df in product_group]
prices = product_group['Price Each'].mean()

plt.bar(products,quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products,rotation='vertical',size=8)
plt.show()


""" 5. what product sold the most"""


product_quantity_data = pd.DataFrame({'Product': products, 'Quantity Ordered': quantity_ordered, 'Price': prices})

product_quantity_data.to_csv('product_quantity_ordered.csv', index=False)


fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity_ordered,color='g')
ax2.plot(products,prices,'b-')
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color='g')
ax2.set_ylabel('Price($)',color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)

plt.show()