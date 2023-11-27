from django.db import models

# Create your models here.
class Logger(models.Model):
    request_ip = models.CharField(max_length=255)
    request_data = models.CharField(max_length=255)
    request_path = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.request_path} --->>> {self.request_ip}'

