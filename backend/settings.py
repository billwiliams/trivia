from dotenv import load_dotenv
import os
load_dotenv()
PROD_DB_NAME = os.environ.get("PROD_DB_NAME")
PROD_DB_USER = os.environ.get("PROD_DB_USER")
PROD_DB_PASSWORD = os.environ.get("PROD_DB_PASSWORD")

# TESTDB

TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
