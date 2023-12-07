from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label="", max_length=140, widget=forms.TextInput(attrs= {
        "class": "form-control mb-3",
        "placeholder": "Title"
    }))
    category = forms.CharField(label="", max_length=140, widget=forms.TextInput(attrs= {
        "class": "form-control mb-3",
        "placeholder": "Category"
    }))
    image = forms.URLField(label="", required=False, widget=forms.TextInput(attrs= {
        "class": "form-control mb-3",
        "placeholder": "Image URL (optional)"
    }))
    description = forms.CharField(label="", widget=forms.Textarea(attrs= {
        "class": "form-control mb-3",
        "placeholder": "Description"
    }))
    starting_bid = forms.FloatField(label="", widget=forms.NumberInput(attrs= {
        "class": "form-control mb3",
        "placeholder": "Starting Price",
        "min": "0.01",
        "step": "0.01"
    }))
