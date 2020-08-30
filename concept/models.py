from django.db import models


class signup(models.Model):
    email = models.TextField()
    username = models.TextField()
    password = models.TextField()
    images = models.TextField()
    date = models.TextField()
    time = models.TextField()
