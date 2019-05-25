from django import forms

MY_CHOICES = (
    ('1', 'Stacje rowerów miejskich'),
)

class DropdownForm(forms.Form):
    my_choice_field = forms.ChoiceField(choices=MY_CHOICES)