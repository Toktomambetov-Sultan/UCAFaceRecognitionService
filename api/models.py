from django.db import models

def imagedir(instance, filename):
    return "static/uploads/images/{}/{}".format(instance._meta.model.__name__+"_"+str(instance.person_id), instance.image.name)
# Create your models here.
class Image(models.Model):   
    uploaded_by = models.PositiveIntegerField(null=True,default=None)
    image = models.ImageField(upload_to=imagedir,     verbose_name="Images|Фотография")
    trained = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Created At|Создано")
    person_id = models.PositiveIntegerField(null=False,unique=False) 
    # is_uploaded_by_security = models.BooleanField(default=False)
    class Meta:
        abstract = True

class StaffImage(Image):
    ...   

class StudentImage(Image):
    ...