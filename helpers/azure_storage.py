from azure.storage.blob import BlobServiceClient
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

