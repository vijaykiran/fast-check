from helper import AzureFileHandler

azure_handler = AzureFileHandler(
    spn_app_id="", spn_password="", tenant_id="", account_url=""
)
CONTAINER = ""


def execute_check(check_id: str, check_json: dict, dataset_location: str) -> dict:
    """
    load the dataset from the passed location using azure library.
    """
    ret_dict = dict()
    data_csv = azure_handler.read_file_from_container_azure(
        container=CONTAINER, file_path=dataset_location
    )

    return ret_dict
