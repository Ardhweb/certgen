from django.db import models

# Create your models here.

    
    
from django.contrib.auth.models import User




import uuid

def get_uuid_only_int_7digits():
    uuid_int = uuid.uuid4().int
    uuid_7digits = uuid_int % 10**7
    return uuid_7digits


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=15, null=True, blank=False, verbose_name='Name')
    issued_at = models.DateField(null=True,blank=True, verbose_name="created_at",editable=True)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateField(null=True,auto_now=True)
    content = models.TextField(null=True,blank=True,max_length=450)
    certificate_no = models.CharField(default=get_uuid_only_int_7digits(), null=True, max_length=7, editable=False)
    header = models.CharField(max_length=20, null=True, blank=True)
    certified_by = models.CharField(max_length=20, null=True, blank=True)

    # def __str__(self):
    #     return self.str(f'{self.name}+{self.user.username}+{self.user.id}')
    
    def get_absolute_url(self):
        return reverse('gen_cert_pdf', args=[self.id])
