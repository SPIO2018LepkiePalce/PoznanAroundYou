from django import forms

MY_CHOICES = (
    ('1', 'Stacje rowerów miejskich'),
)

class DropdownForm(forms.Form):
    wybierz_usługę = forms.ChoiceField(choices=MY_CHOICES)