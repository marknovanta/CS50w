from django.contrib import admin

from .models import User, Transaction, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Contact)
