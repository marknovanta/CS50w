from http.client import HTTPResponse
import random
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown

from . import util

entries_list = util.list_entries()

def index(request):
    if request.method == "POST":
        query = request.POST.get("q")
        for i in entries_list:
            if query == i:
                return render(request, "encyclopedia/show.html", {
                    "entry": markdown.markdown(util.get_entry(query)),
                    "title": query
                })           
        
        #find a match
        low = util.lowering(entries_list)
        matches = list(filter(lambda x: query.lower() in x, low))
        
        #get original names
        print(entries_list)
        c_matches = list()
        for item in matches:
            for original in entries_list:
                if item == original.lower():
                    item = original
                    c_matches.append(item)
        #render them
        return render(request, "encyclopedia/index.html", {
            "entries": c_matches,
            "header": "Search Results"
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "header": "All Pages"
        })

def show(request, title):
    for i in entries_list:
            if title.lower() == i.lower(): # I have to make it case insensitive because chrome keeps changing the URL
                title = i
                return render(request, "encyclopedia/show.html", {
                    "entry": markdown.markdown(util.get_entry(title)),
                    "title": title
                })
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page was not found"
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="", widget=forms.Textarea())


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
                "form": NewPageForm()
            })
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                entries_list.append(title)
                return render(request, "encyclopedia/show.html", {
                    "entry": markdown.markdown(util.get_entry(title)),
                    "title": title
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "This entry already exists"
                })

def edit_page(request):
    if request.method == "GET":
        form = NewPageForm()
        title = request.GET["title"]
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "form": form
            })
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/show.html", {
                "entry": markdown.markdown(util.get_entry(title)),
                "title": title
            })

def random_page(request):
    title = random.choice(entries_list)
    return render(request, "encyclopedia/show.html", {
                    "entry": markdown.markdown(util.get_entry(title)),
                    "title": title
                }) 