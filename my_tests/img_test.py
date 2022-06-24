import requests
from django.core.files.base import ContentFile


def get(img_url):
    image_content = ContentFile(requests.get(img_url).content)
    print('image_content', image_content)
    print('image_content', image_content.name)
    print('image_content', image_content.file)


if __name__ == '__main__':
    get('https://telegram.botframework.com/v3/attachments/weurope:at51873-6GP3qksz4vr/views/original')