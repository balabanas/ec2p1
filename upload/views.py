import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .models import Upload, UploadPrivate


def image_upload(request):
    print('Im at the top of image_upload view')
    if request.method == 'POST':
        print('before setting file image, file image type')
        image_file = request.FILES['image_file']
        print(dir(request))
        image_type = request.POST['image_type']
        print('before checking if settings USE3')
        print('settings.USE_S3', settings.USE_S3)
        if settings.USE_S3:
            print('I am gere (before creating image instance)')
            if image_type == 'private':
                upload = UploadPrivate(file=image_file)
            else:
                upload = Upload(file=image_file)
            upload.save()
            image_url = upload.file.url
        else:
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
        return render(request, 'upload/upload.html', {
            'image_url': image_url
        })
    return render(request, 'upload/upload.html', {'debug': settings.DEBUG})
