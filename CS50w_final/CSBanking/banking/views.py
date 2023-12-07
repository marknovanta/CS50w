from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F, Q, When
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Transaction, Contact


# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, "banking/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "banking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "banking/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "banking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "banking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "banking/register.html")

@login_required(login_url='login')
def get_balance(request):
    user = User.objects.get(id=request.user.id)
    return JsonResponse(user.serialize())

@login_required(login_url='login')
def get_contacts(request):
    contacts = Contact.objects.filter(user=request.user).order_by("contact").all()
    return JsonResponse([contact.serialize() for contact in contacts], safe=False)
    
@login_required(login_url='login')
def add_contact(request):
    data = json.loads(request.body)
    check = User.objects.all().filter(username=data['contact'])
    if len(check) == 0:
        return JsonResponse({'error': 'user not found'})
    else:
        user_to_add = User.objects.get(username=data['contact'])
        contact = Contact(user=request.user, contact=user_to_add)
        contact.save()
        return JsonResponse({'message': 'success'})


@login_required(login_url='login')
def remove_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.delete()
    return JsonResponse({'message': 'success'})

@login_required(login_url='login')
def transfer(request):
    data = json.loads(request.body)
    
    #subtract cash from user
    user = User.objects.get(id=request.user.id)

    #check if enough cash
    if user.balance < float(data['amount']):
        return JsonResponse({'error': 'not enough cash'})
    else:
        user.balance -= float(data['amount'])
        user.save()

    #add cash to receiver
    receiver = User.objects.get(username=data['receiver'])
    receiver.balance += float(data['amount'])
    receiver.save()

    #record transaction
    now = datetime.now()
    receiver = User.objects.get(username=data['receiver'])
    t = Transaction(sender=request.user, receiver=receiver, amount=data['amount'], timestamp=now)
    t.save()
    return JsonResponse({'message': 'success'})

@login_required(login_url='login')
def get_transactions(request):
    transactions = Transaction.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id)).order_by("-id").all()
    return JsonResponse([transaction.serialize() for transaction in transactions], safe=False)

@login_required(login_url='login')
def get_user(request):
    return JsonResponse({'user': request.user.username})

@login_required(login_url='login')
def add_cash(request):
    data = json.loads(request.body)

    try:
        amount = float(data['amount'])
    except:
        return JsonResponse({'error': "something went wrong"})
    if not data['amount']:
        return JsonResponse({'error': "something went wrong"})
    elif float(data['amount']) < 0:
        return JsonResponse({'error': "something went wrong"})
    
    #add cash to the balance
    user = User.objects.get(id=request.user.id)
    user.balance += amount
    user.save()

    #record transaction
    now = datetime.now()
    t = Transaction(sender=user, receiver=user, amount=data['amount'], timestamp=now)
    t.save()

    return JsonResponse({'message': "success"})