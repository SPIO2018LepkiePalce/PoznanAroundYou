from django import forms

MY_CHOICES = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)

class DropdownForm(forms.Form):
    my_choice_field = forms.ChoiceField(choices=MY_CHOICES)