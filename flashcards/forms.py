from django import forms

class Registration(forms.Form):
	e_mail = forms.EmailField(label="E-mail")
	password = forms.PasswordField()

class Create_deck(forms.Form):
	deck_name = forms.CharField(label="Название", max_length=30)
	repeat_time = forms.