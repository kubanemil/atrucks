"""
This script should be launched in AWS Lambda to parse the data 
from the site and insert it into the database once a day.
"""

import logging
import os

import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

# db
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
TABLE_NAME = "phone_phoneinfo"

URL = "https://opendata.digital.gov.ru/registry/numeric/downloads"
CSV_URL = "https://opendata.digital.gov.ru/downloads/"


def download_files():
    response = requests.get(URL)
    if response.status_code != 200:
        logging.error(f"Failed to download the page: {URL}")
        raise response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and CSV_URL in href:
            response = requests.get(href)

            if response.status_code != 200:
                logging.error(f"Failed to download the file from {href}")
                response.raise_for_status()

            os.makedirs("csv", exist_ok=True)
            file_name = href.split("/")[-1].split("?")[0]
            with open(f"csv/{file_name}", "wb") as f:
                f.write(response.content)


def insert_with_pandas(fn):
    df = pd.read_csv(fn, sep=";")
    df.drop(["Емкость", "Территория ГАР", "ИНН"], axis=1, inplace=True)
    df.rename(
        columns={
            df.columns[0]: "abc_code",
            "От": "min_code",
            "До": "max_code",
            "Оператор": "operator",
            "Регион": "region",
        },
        inplace=True,
    )

    with psycopg2.connect(
        database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    ) as conn:
        cur = conn.cursor()

        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        query = f"""
           INSERT INTO {TABLE_NAME} ({columns}) 
            VALUES ({placeholders})
            ON CONFLICT (abc_code, min_code, max_code)
            DO UPDATE SET 
                operator = EXCLUDED.operator, 
                region = EXCLUDED.region
            WHERE {TABLE_NAME}.operator <> EXCLUDED.operator OR {TABLE_NAME}.region <> EXCLUDED.region;
        """

        values = [tuple(x) for x in df.to_numpy()]

        logging.info(f"Inserting {len(df)} rows into table {TABLE_NAME}...")
        cur.executemany(query, values)
        conn.commit()
        logging.info("Done")


def lambda_handler(event, context):
    logging.debug(event)
    logging.debug(context)

    # download_files()
    for fn in os.listdir("csv"):
        logging.info(f"Inserting for file {fn}")
        insert_with_pandas(f"csv/{fn}")


if __name__ == "__main__":
    lambda_handler(None, None)
