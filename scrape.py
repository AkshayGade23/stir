import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import uuid
from datetime import datetime
import json
import requests

# Free ProxyMesh servers



uri = "my mongo uri"

def test_proxy(proxy):
    """Test if the proxy is working"""
    try:
        response = requests.get(
            'http://www.google.com',
            proxies={'http': proxy, 'https': proxy},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def fetch_trending_topics():
   
    # Set up the WebDriver with the working proxy
    driver = webdriver.Chrome()
    print("aaaaa")
    # driver.set_page_load_timeout(30)
    
    try:
        driver.get('https://twitter.com/explore')
        time.sleep(80)  # Wait for trends to load
        
        print("bbbb")
        trending_topics = driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")
        trends = [topic.text for topic in trending_topics[:5]]  # Changed to get 5 trends
        
        # Generate unique ID and timestamp
        unique_id = str(uuid.uuid4())
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract IP address from proxy
        response = requests.get('https://api.ipify.org')
        ip_address = response.text
        
        
        # MongoDB Connection
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["twitter_trends"]
        collection = db["trends"]
        
        # Store exactly the required fields
        data = {
            "_id": unique_id,
            "trend1": trends[0] if len(trends) > 0 else None,
            "trend2": trends[1] if len(trends) > 1 else None,
            "trend3": trends[2] if len(trends) > 2 else None,
            "trend4": trends[3] if len(trends) > 3 else None,
            "trend5": trends[4] if len(trends) > 4 else None,
            "end_time": end_time,
            "ip_address": ip_address  # Changed from proxy_used to ip_address
        }
        
        collection.insert_one(data)
        driver.quit()
        return data
        
    except Exception as e:
        driver.quit()
        raise e

def fetch_data_mongo():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["twitter_trends"]
    collection = db["trends"]
    
    latest_record = collection.find_one(sort=[('end_time', -1)])
    return latest_record




# def fetch_trending_topics():
#     # Randomly select a proxy for each request
#     # proxy = random.choice(PROXY_LIST)
#     # options = webdriver.ChromeOptions()
#     # options.add_argument(f'--proxy-server={proxy}')

#     # Set up the WebDriver
#     driver = webdriver.Chrome()
#     driver.get('https://twitter.com/login')

#     # Log in to Twitter (Provide your credentials)
#     # username = "akshaygade2327@gmail.com"
#     # password = "IlajnaPower@2327"

#     time.sleep(60)  # Adjust as per your internet speed

#     # Fetch trending topics
#     trending_topics = driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")
#     trends = [topic.text for topic in trending_topics[:4]]

#     print("dsafsdfsd")
#     print(trends)
#     print("fdfd")

#     # Generate unique ID and timestamp
#     unique_id = str(uuid.uuid4())
#     end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     # ip_address = proxy.split('@')[1].split(':')[0]

#     # MongoDB Connection
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     db = client["twitter_trends"]
#     collection = db["trends"]

#     data = {
#         "_id": unique_id,
#         "trend1": trends[0],
#         "trend2": trends[1],
#         "trend3": trends[2],
#         "trend4": trends[3],
#         # "trend5": trends[4],
#         "end_time": end_time,
#         # "ip_address": ip_address
#     }
#     collection.insert_one(data)
#     driver.quit()
#     return data

# def fetch_data_mongo():
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     db = client["twitter_trends"]
#     collection = db["trends"]

#     latest_record = collection.find_one(sort=[('_id', -1)])
#     return latest_record

# Use ProxyMesh such that each new request to scrape the trending topics is sent from a new IP address.