from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

class AskForm(forms.Form):
	title = forms.CharField(max_length=255)
	text = forms.CharField(widget=forms.Textarea)

	def save(self):
		if self._user is not None:
			self.cleaned_data['author'] = self._user
		return Question.objects.create(**self.cleaned_data)
	
class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput())

	def save(self):
		if self._user is not None:
			self.cleaned_data['author'] = self._user
		self.cleaned_data['question_id'] = self.cleaned_data['question']
		del(self.cleaned_data['question'])
		return Answer.objects.create(**self.cleaned_data)

class SignupForm(forms.Form):
	username = forms.CharField(max_length=255)
	email = forms.EmailField()
	password = forms.PasswordInput()

	def save(self):
		user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
		return user

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255)
	password = forms.PasswordInput()

	def save(self):
		user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
		return user