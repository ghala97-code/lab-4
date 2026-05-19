from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0) 
    quantity = models.IntegerField(default=1) 
    pubdate = models.DateTimeField()
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL) 
    authors = models.ManyToManyField(Author) 



class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.street}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Address2(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.street}"

class Student2(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # ManyToManyField
    addresses = models.ManyToManyField(Address2) 

    def __str__(self):
        return self.name 

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.title
    
