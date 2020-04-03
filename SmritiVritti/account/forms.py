from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from django.db import models
class AddUserForm(forms.ModelForm):
	"""
	New User Form. Requires password confirmation.
	"""
	username=forms.CharField(max_length=255,widget=forms.TextInput(
		attrs={ 'placeholder':"email_or_phone" }),
		label="email_or_phone",
		)

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput,)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput,  )
	#email_or_phone = forms.CharField(label='email_or_phone', )
	class Meta:
		model = User
		fields =('username',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password2
	

	def save(self, commit = True):
		# Save the provided password in hashed format
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password1"])
		email_or_phone = self.cleaned_data['username']
		

		if not email_or_phone:
			raise ValueError('The given email_or_phone must be set')

		if "@" in email_or_phone:
			#email_or_phone = self.normalize_email(email_or_phone)
			user.email, user.phone = email_or_phone, ""
		else:
			
			user.email, user.mobile_no = "", email_or_phone

		
		if commit:

			user.save()
		


		
		

		return user



class UpdateUserForm(forms.ModelForm):
	"""
	Update User Form. Doesn't allow changing password in the Admin.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = (
			'email', 'password', 'is_active',
			'is_staff'
		)

	def clean_password(self):
# Password can't be changed in the admin
		return self.initial["password"]
