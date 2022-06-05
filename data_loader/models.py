from django.db import models


class Company(models.Model):
    """
    Model to hold companies.
    Schema was decided according to the design provided in
    the json file. Using index and company name.
    As index started from 0 in given data (json), it could not be used as primary key.
    """
    index = models.IntegerField()
    company = models.CharField(max_length=20)

    def __str__(self):
        return self.company


class Person(models.Model):
    """
    Model to hold People.
    Schema was decided according to the questions, some fields were skipped.
    As index started from 0 in given data (json), it could not be used as primary key.
    """
    index = models.IntegerField()
    guid = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    eye_color = models.CharField(max_length=20)
    has_died = models.BooleanField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class PersonFriend(models.Model):
    """
    Person table needed a many to many relation with itself. Hence PersonFriend table was
    created as a join table to hold the relation.
    """
    person_id = models.ForeignKey(Person, related_name='Person', on_delete=models.CASCADE)
    friend_id = models.ForeignKey(Person, related_name='PersonFriend', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.person_id)


class Fruit(models.Model):
    """
    Model to hold fruits.
    As fruits.json was not provided, the table schema is assumed to hold only the fruit name.
    Fruit table has many to many relation with Person. The join table is created automatically.
    """
    fruit_name = models.CharField(max_length=20)
    person = models.ManyToManyField(Person, null=True, blank=True)

    def __str__(self):
        return self.fruit_name


class Vegetable(models.Model):
    """
    Model to hold vegetables.
    As vegetable.json was not provided, the table schema is assumed to hold only the vegetable name.
    Vegetable table has many to many relation with Person. The join table is created automatically.
    """
    vegetable_name = models.CharField(max_length=20)
    person = models.ManyToManyField(Person, null=True, blank=True)

    def __str__(self):
        return self.vegetable_name
