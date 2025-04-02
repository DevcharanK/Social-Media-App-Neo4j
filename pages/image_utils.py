from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import os
import config
import uuid

AZURE_CONNECTION_STRING = config.AZURE_STORAGE_CONNECTION_STRING
CONTAINER_NAME = config.CONTAINER_NAME
blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(config.CONTAINER_NAME)

############################################
# Image Upload and Management Functions    #
############################################

## Upload an image to Azure Blob Storage and return the URL
def upload_post_image(uploaded_file):
    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_name = CONTAINER_NAME  # Folder to store post images

    # Generate a unique filename based on the post ID 
    filename = f"post_images/post_image_{str(uuid.uuid4())}.jpg"

    # Determine the content type based on the file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()

    # Map the file extension to the appropriate content type
    if file_extension == "jpg" or file_extension == "jpeg":
        content_type = "image/jpeg"
    elif file_extension == "png":
        content_type = "image/png"
    elif file_extension == "gif":
        content_type = "image/gif"
    elif file_extension == "bmp":
        content_type = "image/bmp"
    else:
        content_type = "application/octet-stream"  # Default content type for unknown formats


    # Upload the image to Azure Storage Blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    
    # Upload the file to Azure blob storage
    blob_client.upload_blob(uploaded_file, overwrite=True, content_settings=ContentSettings(content_type=content_type))

    # Generate and return the image URL
    image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}"
    return image_url

#Upload profile image to Azure Blob Storage and return the URL
def upload_profile_image(uploaded_file):
   # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_name = CONTAINER_NAME  # Folder to store post images

    # Generate a unique filename 
    filename = f"profile_images/profile_image_{str(uuid.uuid4())}.jpg"

    # Determine the content type based on the file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()

    # Map the file extension to the appropriate content type
    if file_extension == "jpg" or file_extension == "jpeg":
        content_type = "image/jpeg"
    elif file_extension == "png":
        content_type = "image/png"
    elif file_extension == "gif":
        content_type = "image/gif"
    elif file_extension == "bmp":
        content_type = "image/bmp"
    else:
        content_type = "application/octet-stream"  # Default content type for unknown formats


    # Upload the image to Azure Storage Blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    
    # Upload the file to Azure blob storage
    blob_client.upload_blob(uploaded_file, overwrite=True, content_settings=ContentSettings(content_type=content_type))

    # Generate and return the image URL
    image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}"
    return image_url
    
def delete_image(file_name):
    """Delete an image from the Azure Blob Storage container."""
    try:
        # Create a blob client using the file name
        blob_client = container_client.get_blob_client(file_name)

        # Delete the blob
        blob_client.delete_blob()
        print(f"✅ Image {file_name} deleted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error deleting image: {e}")
        return False

def generate_image_url(file_name):
    """Generate a URL for the image stored in Azure Blob Storage."""
    try:
        # Create a blob client using the file name
        blob_client = container_client.get_blob_client(file_name)

        # Generate a URL for the blob
        url = blob_client.url
        print(f"✅ Image URL generated: {url}")
        return url
    except Exception as e:
        print(f"❌ Error generating image URL: {e}")
        return None

def download_image(file_name, download_path):
    """Download an image from Azure Blob Storage to a local path."""
    try:
        # Create a blob client using the file name
        blob_client = container_client.get_blob_client(file_name)

        # Download the blob to a local file
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
            print(f"✅ Image {file_name} downloaded successfully to {download_path}!")
            return True
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return False
    
if __name__ == "__main__":
    #Test generate_image_url function
    file_name = "test_image.jpg"
    url = generate_image_url(file_name)
    if url:
        print(f"Image URL: {url}")
    else:
        print("Failed to generate image URL.")