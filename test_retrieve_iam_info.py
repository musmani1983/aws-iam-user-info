import unittest
import os
import json
import csv
from retrieve_iam_user_info import retrieve_iam_user_info, write_to_csv, write_to_json

class TestRetrieveIAMUserInfo(unittest.TestCase):

    def setUp(self):
        # Set up AWS environment variables for testing
        os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'
        os.environ['AWS_SESSION_TOKEN'] = 'your_session_token'

    def test_retrieve_iam_user_info(self):
        iam_user_info = retrieve_iam_user_info()

        # Ensure that IAM user information is retrieved
        self.assertTrue(len(iam_user_info) > 0)

        # Check if 'AccessKeys' column contains consolidated access key details
        for user_info in iam_user_info:
            access_keys = user_info.get('AccessKeys', '')
            self.assertTrue(isinstance(access_keys, str))
            self.assertTrue(len(access_keys) > 0)

    def test_write_to_csv(self):
        iam_user_info = retrieve_iam_user_info()
        csv_file_name = 'test_iam_user_info.csv'
        write_to_csv(iam_user_info, csv_file_name)

        # Ensure that the CSV file is created
        self.assertTrue(os.path.exists(csv_file_name))

        # Read the CSV file and check if it contains data
        with open(csv_file_name, 'r') as csvfile:
            csv_data = list(csv.DictReader(csvfile))
            self.assertTrue(len(csv_data) > 0)

    def test_write_to_json(self):
        iam_user_info = retrieve_iam_user_info()
        json_file_name = 'test_iam_user_info.json'
        write_to_json(iam_user_info, json_file_name)

        # Ensure that the JSON file is created
        self.assertTrue(os.path.exists(json_file_name))

        # Read the JSON file and check if it contains data
        with open(json_file_name, 'r') as jsonfile:
            json_data = json.load(jsonfile)
            self.assertTrue(len(json_data) > 0)

if __name__ == '__main__':
    unittest.main()
