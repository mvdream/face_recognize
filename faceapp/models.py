from django.db import models

class Datasets(models.Model):
    encoding = models.TextField()
    label = models.IntegerField()

class People(models.Model):
    label_id = models.IntegerField()
    name = models.CharField(max_length=100)