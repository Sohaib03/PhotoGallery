from django.db import models
from django.conf import settings


import os
import firebase_admin
from firebase_admin import credentials, initialize_app, storage


cred = credentials.Certificate('API_CONFIG/config.json')
default_app = initialize_app(cred, {'storageBucket': 'photogallery-d484b.appspot.com'})

bucket = storage.bucket()
print(default_app.name)


def handle_upload_file(file):
    path = os.path.join(settings.BASE_DIR, 'media', str(file))
    try:
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except FileNotFoundError:
        os.mkdir('media')
        handle_upload_file(file)
    return path

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name

class PhotoQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            print("\n**** Deleting Photo ****\n")

            blob = bucket.blob(blob_name=str(obj.image))
            blob.delete()

            print("Deleted\n")

        super(PhotoQuerySet, self).delete(*args, **kwargs)

class Photo(models.Model):

    objects = PhotoQuerySet.as_manager()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        print("Saving photo")
        path = handle_upload_file(self.image)
        blob = bucket.blob(blob_name=str(self.image))
        blob.upload_from_filename(path)
        blob.make_public()

        print("Local Path::", path)
        os.remove(path)

        self.url = blob.public_url

        print("IMAGE::",type(self.image), "URL : ", blob.public_url)
        super(Photo, self).save(*args, **kwargs)

        local_store_path = os.path.join(settings.BASE_DIR, 'static\images', str(self.image))

        os.remove(local_store_path)

    def delete(self, *args, **kwargs):
        print("\n**** Deleting Photo ****\n")

        blob = bucket.blob(blob_name=str(self.image))
        blob.delete()

        print("Deleted\n")

        super(Photo, self).delete(*args, **kwargs)