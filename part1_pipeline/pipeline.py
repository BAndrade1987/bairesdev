import requests
import pandas as pd
import logging
import time
import json
import os
from dotenv import load_dotenv
import argparse

load_dotenv()

apiUsers = os.getenv("API_USERS_URL")
apiPosts = os.getenv("API_POSTS_URL")
retries = int(os.getenv("RETRIES", 3))
timeout = int(os.getenv("TIMEOUT", 5))

with open("config.json", "r") as f:
    config = json.load(f)

outputFile = config["output_file"]

logging.basicConfig(
    filename=config["log_file"],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetchData(url):
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Fetching data from {url} (attempt {attempt})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            if attempt < retries:
                time.sleep(2)
            else:
                raise Exception(f"Fail after {retries} attempt")

def extractData():
    users = fetchData(apiUsers)
    posts = fetchData(apiPosts)
    return users, posts

def transformData(users, posts):
    dfUsers = pd.json_normalize(users)
    dfPosts = pd.json_normalize(posts)

    dfUsers = dfUsers[[
        "id", "name", "email", "address.city", "company.name"
    ]]
    dfUsers.columns = ["userId", "name", "email", "city", "company"]

    postCounts = dfPosts.groupby("userId").size().reset_index(name="totalPosts")
    postCounts.rename(columns={"userId": "userId"}, inplace=True)

    processed = dfUsers.merge(postCounts, on="userId", how="left")
    return processed

def loadData(df):
    df.to_csv(outputFile, index=False)
    logging.info(f"File saved: {outputFile}")
    print(f"Arquivo salvo: {outputFile}")

def runPipeline():
    logging.info("Start ETL")
    try:
        users, posts = extractData()
        df = transformData(users, posts)
        loadData(df)
        logging.info("Pipeline complted.")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print("Error.")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline.")
    args = parser.parse_args()
    runPipeline()