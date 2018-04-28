from django import forms

class RegisterForm(forms.Form):
	name = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control form-control-sm'}),label="Enter Your Name :")
	email = forms.CharField(widget = forms.EmailInput(attrs={'class' : 'form-control form-control-sm','placeholder':'example@gmail.com'}),label="Enter Mail Id :")
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class' : 'form-control form-control-sm'}), label="Enter Password :")
	repassword = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control form-control-sm'}),label="Confirm Password :")
	phone_no = forms.CharField(widget = forms.TextInput(attrs={'class' : 'form-control form-control-sm','placeholder':'+91 9999999'}),label="Enter Phone Number :")

class LoginForm(forms.Form):
	email = forms.CharField(widget = forms.EmailInput(attrs={'class' : 'form-control form-control-sm'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class' : 'form-control form-control-sm'}))


