import argparse
import os
import boto3
import csv
import json

def retrieve_iam_user_info():
    # Retrieve AWS credentials from environment variables
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
    
    # Initialize the AWS client
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )
    iam_client = session.client('iam')

    # Retrieve and process IAM users
    response = iam_client.list_users()

    user_info_list = []

    for user in response['Users']:
        user_name = user['UserName']
        user_id = user['UserId']
        create_date = user['CreateDate']
        user_arn = user['Arn']

        # Retrieve password last changed date
        password_last_changed = iam_client.get_user(UserName=user_name)['User']['PasswordLastUsed']

        # Retrieve and process access keys
        access_keys_response = iam_client.list_access_keys(UserName=user_name)
        access_key_details = []

        for key in access_keys_response['AccessKeyMetadata']:
            access_key_id = key['AccessKeyId']
            status = key['Status']
            key_create_date = key['CreateDate']

            # Calculate key age
            key_age = (create_date - key_create_date).days

            # Retrieve and process access key last used data
            access_key_last_used = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
            last_used_date = access_key_last_used['AccessKeyLastUsed'].get('LastUsedDate', 'N/A')

            access_key_detail = {
                'AccessKeyId': access_key_id,
                'Status': status,
                'CreateDate': key_create_date.isoformat(),
                'KeyAge': key_age,
                'LastUsedDate': last_used_date.isoformat() if last_used_date != 'N/A' else 'N/A'
            }
            access_key_details.append(access_key_detail)

        user_info = {
            'UserName': user_name,
            'UserId': user_id,
            'CreateDate': create_date.isoformat(),
            'Arn': user_arn,
            'PasswordLastChanged': password_last_changed.isoformat(),
            'AccessKeys': access_key_details  # Consolidate access key details
        }

        user_info_list.append(user_info)

    return user_info_list

def write_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Combine access key details into a single column
            row['AccessKeys'] = ', '.join([f"{key['AccessKeyId']} (Status: {key['Status']}, Age: {key['KeyAge']} days, Last Used: {key['LastUsedDate']})"
                                            for key in row['AccessKeys']])
            writer.writerow(row)

def write_to_json(data, file_name):
    with open(file_name, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve IAM user information.')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format (csv or json)')
    args = parser.parse_args()

    iam_user_info = retrieve_iam_user_info()

    if args.format == 'csv':
        csv_file_name = 'iam_user_info.csv'
        write_to_csv(iam_user_info, csv_file_name)
        print(f'IAM user information saved to {csv_file_name}')
    elif args.format == 'json':
        json_file_name = 'iam_user_info.json'
        write_to_json(iam_user_info, json_file_name)
        print(f'IAM user information saved to {json_file_name}')
