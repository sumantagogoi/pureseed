from django.db import models

# Create your models here.


class ResetPasswordToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.email} {self.token}'
