import sys
import uuid
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.
class UsrGender(models.Model):
    gender_name = models.CharField(max_length=20)
    gender_initial = models.CharField(max_length=1)
    gender_detail = models.CharField(max_length=80)
    gender_code = models.CharField(max_length=15)

    class Meta:
        db_table = "usr_gender"


class UsrUser(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    username = models.CharField(max_length=20)
    user_code = models.CharField(max_length=15)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='images/profile_images/', null=True)
    gender = models.ForeignKey(UsrGender, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=125)

    def save(self, *args, **kwargs):
        if self.profile_image:
            image = Image.open(self.profile_image)
            bytes_img = BytesIO()
            check_size = self.profile_image.size / 1024 # noqa
            if check_size > 1024:
                image.resize((1024, 1024))
            image.save(bytes_img, format='JPEG', quality=60)
            bytes_img.seek(0)
            # What if user uploads the same name image so Universal Unique ID
            self.profile_image = InMemoryUploadedFile(bytes_img, 'ImageField', "%s.jpg" % str(uuid.uuid4()),
                                                      'profile_image.jpeg', sys.getsizeof(bytes_img), None)
        super(UsrUser, self).save()

    class Meta:
        db_table = "usr_user"
