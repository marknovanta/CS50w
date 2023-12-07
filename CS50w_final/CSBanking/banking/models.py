from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    balance = models.FloatField(default=0)


    def serialize(self):
        return {
            "id": self.id,
            "balance": self.balance,
            "username": self.username
        }


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')
    amount = models.FloatField()
    timestamp = models.DateField(auto_now=True)

    def serialize(self):
        return {
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "amount": self.amount,
            "timestamp": self.timestamp
        }


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts_added')

    def serialize(self):
        return {
            "id": self.id,
            "contact": self.contact.username,
        }