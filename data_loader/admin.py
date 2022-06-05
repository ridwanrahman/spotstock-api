from django.contrib import admin

from .models import Company, Person, Fruit, Vegetable, PersonFriend

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(PersonFriend)
admin.site.register(Fruit)
admin.site.register(Vegetable)
