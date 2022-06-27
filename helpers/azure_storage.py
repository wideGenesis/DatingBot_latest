import os

from azure.storage.blob import BlobServiceClient, BlobClient
from settings.conf import AZURE_STORAGE_CONF
from settings.logger import CustomLogger

logger = CustomLogger.get_logger('bot')

service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONF.STORAGE_CONNECTION_STRING)
client = service_client.get_container_client(AZURE_STORAGE_CONF.BLOB_CONTAINER_NAME)


def rm_blobs():
    blobsToDelete = []
    count_blobs = []
    try:
        for blobs in client.list_blobs():
            blobsToDelete.append(blobs.name)
            count_blobs.append(blobs.name)
            client.delete_blobs(*blobsToDelete)
            blobsToDelete.clear()
    except Exception:
        logger.exception('Error while deleting blobs')
        blobsToDelete.clear()
        pass

    logger.info(
        '%s blobs has been removed from container: %s, account: %s',
        len(count_blobs),
        AZURE_STORAGE_CONF.BLOB_CONTAINER_NAME,
        AZURE_STORAGE_CONF.STORAGE_ACCOUNT_NAME
    )
    return


def rm_user_blobs(member_id: str):
    blobsToDelete = [f'telegram/conversations/{member_id}', f'telegram/users/{member_id}']
    try:
        client.delete_blobs(*blobsToDelete)
        blobsToDelete.clear()
    except Exception:
        logger.exception('Error while deleting blobs')
        blobsToDelete.clear()
        pass


# ---------------------------------------------------------------------------------------------------------
# https://docs.microsoft.com/ru-ru/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows
# ----------------------------------------------------------------------------------------------------------

async def upload_blob(filename: str, member_id: str) -> bool:
    local_file_path = os.path.join('ms_bot', 'temp_media', filename)
    blob = 'video_{}'.format(filename)
    container = 'media/tg_{}/'.format(member_id, filename)

    # Create a blob client using the local file name as the name for the blob
    blob_client = service_client.get_blob_client(container=container, blob=blob)

    # Upload the created file
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)
    logger.debug("\nUpload to Azure Storage as blob has been successful:\n\t" + blob)

    return True
