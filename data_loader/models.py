from django.db import models


class Company(models.Model):
    index = models.IntegerField()
    company = models.CharField(max_length=20)

    def __str__(self):
        return self.company


class Person(models.Model):
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
    person_id = models.ForeignKey(Person, related_name='Person', on_delete=models.CASCADE)
    friend_id = models.ForeignKey(Person, related_name='PersonFriend', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.person_id)


class Fruit(models.Model):
    fruit_name = models.CharField(max_length=20)
    person = models.ManyToManyField(Person)

    def __str__(self):
        return self.fruit_name


class Vegetable(models.Model):
    vegetable_name = models.CharField(max_length=20)
    person = models.ManyToManyField(Person)

    def __str__(self):
        return self.vegetable_name
