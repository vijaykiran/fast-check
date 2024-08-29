from azure import identity
from azure.storage.blob import BlobServiceClient


class AzureFileHandler:
    def __init__(
        self,
        spn_app_id: str,
        spn_password: str,
        tenant_id: str,
        account_url: str,
    ) -> None:
        self.spn_app_id = spn_app_id
        self.spn_password = spn_password
        self.tenant_id = tenant_id
        self.account_url = account_url

        self.credential = identity.ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.spn_app_id,
            client_secret=self.spn_password,
        )
        self.blob_service_client = BlobServiceClient(
            account_url=self.account_url, credential=self.credential
        )

    def read_file_from_container_azure(
        self,
        container: str,
        file_path: str,
    ) -> bytes:
        container_client = self.blob_service_client.get_container_client(
            container=container
        )
        blob_client = container_client.get_blob_client(file_path)
        blob_data = blob_client.download_blob().readall()
        return blob_data

    def write_file_to_azure(
        self,
        container: str,
        data: str,
        filename: str,
    ):
        container_client = self.blob_service_client.get_container_client(
            container=container
        )
        blob_client = container_client.get_blob_client(blob=filename)
        blob_client.upload_blob(data, overwrite=True)
