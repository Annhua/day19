from django.db import models

# Create your models here.
class Publish(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Classfication(models.Model):
    name=models.CharField(max_length=32,default='文学类')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publish)
    classes=models.ForeignKey(Classfication,default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    def __str__(self):
        return self.title
