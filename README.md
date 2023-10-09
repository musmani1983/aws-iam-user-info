# AWS IAM User Info Retrieval

This Python script allows you to retrieve information about AWS IAM users, including details such as user attributes, access keys, and their status, and save the data in either CSV or JSON format.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3 installed
- `boto3` library installed (you can install it via `pip install boto3`)
- AWS CLI configured with the necessary credentials

## Usage

### Setting Up the Environment

To set up the virtual environment and install dependencies, run:

```shell
make setup
```

### Running the Script

You can run the script with the following commands:

- To retrieve IAM user information and save it as CSV (default):

  ```shell
  make run-csv
  ```

- To retrieve IAM user information and save it as JSON:

  ```shell
  make run-json
  ```

### Running Tests

To run tests using `unittest`, execute:

```shell
make test
```

### Help

For more information on available targets and their descriptions, use:

```shell
make help
```

## Directory Structure

- `retrieve_iam_user_info.py`: Python script to retrieve IAM user information.
- `test_retrieve_iam_user_info.py`: Unit tests for the script.
- `requirements.txt`: List of required Python packages.
- `Makefile`: Configuration for running tests and the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you find any issues or have suggestions for improvements.

## Acknowledgments

- Special thanks to the [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library for making AWS interactions in Python easy.
