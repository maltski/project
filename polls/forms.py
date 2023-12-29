from django import forms


class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())