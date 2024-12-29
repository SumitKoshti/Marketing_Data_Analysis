#!/usr/bin/env python
# coding: utf-8

# # SENTIMENT ANALYSIS :

# In[8]:


# Importing the libraries

import pandas as pd
import numpy as np
import pyodc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import mysql.connector


# In[ ]:





# In[7]:


# Installing the sql-python connector
pip install mysql-connector-python


# In[ ]:





# In[5]:


nltk.download("vader_lexicon")


# In[ ]:





# ## Final Script :

# In[36]:


import mysql.connector
import pandas as pd 
import pyodbc

def fetch_data_from_mysql():
    try:
        # Establish the connection to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            username="root",
            password="pksumit100",
            database="marketing_db"
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            
        
        conn = connection  # Use the connection directly
        
        # SQL query to fetch data
        query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM customer_reviews"
        
        # Read data into a pandas DataFrame
        df = pd.read_sql(query, conn)
        
        # Return the DataFrame
        return df
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
    finally:
        # Ensure the connection is closed
        if conn.is_connected():
            conn.close()
            print("MySQL connection closed")

# Call the function to fetch data
customer_reviews_df = fetch_data_from_mysql()

# Print the DataFrame to see the result
print(customer_reviews_df)


# In[ ]:





# In[26]:


# Define sentiment intensity analyzer
sa = SentimentIntensityAnalyzer()


# ## Defining Functions : 

# In[31]:



# 1.
def calculate_sentiment(review):
    sentiment= sa.polarity_scores(review)
    return sentiment["compound"]

# 2.
def sentiment_categories(score, rating):
    if score > 0.05:   # Positive sentiment score            
        if rating >=4:
            return "Positive"    # High rating and positive sentiment
        elif rating ==3:
            return "Mixed Positive"   # Neutral rating but positive sentiment
        else:
            return "Mixed Negative"   # Low rating but positive sentiment
    elif score < -0.05: # Negative sentiment score
        if rating <=2:
            return "Negative"   # Low rating and negative sentiment
        elif rating == 3:
            return "Mixed Negative"   # Neutral rating but negative sentiment
        else: 
            return "Mixed Positive"  # High rating but negative sentiment
    else:     # Neutral sentiment score (>-0.05 And <0.05)
        if rating >=4:  
            return "Positive"   # High rating with neutral sentiment
        elif rating <=2:
            return "Negative"    # Low rating with neutral sentiment
        else:
            return "Neutral"   # Neutral rating and neutral sentiment
# 3.       
def sentiment_bucket(score):
    if score >= 0.5:         
        return "0.5 to 1.0"    # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return "0.0 to 0.49"   # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return "-0.49 to 0.0"  # Mildly negative sentiment
    else:
        return "-1.0 to -0.5"  # Strongly negative sentiment

# Calculations
customer_reviews_df["SentimentScore"] = customer_reviews_df["ReviewText"].apply(calculate_sentiment)

customer_reviews_df["SentimentCategory"] = customer_reviews_df.apply(
    lambda row: sentiment_categories(row["SentimentScore"], row["Rating"]),axis=1)

customer_reviews_df["SentimentBucket"] = customer_reviews_df["SentimentScore"].apply(sentiment_bucket)

print(customer_reviews_df.head())




# In[ ]:





# ## Convert into CSV Format :

# In[32]:


# Convert data into csv format
customer_reviews_df.to_csv("customer_reviews_with_sentiment.csv", index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




