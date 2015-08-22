from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
def main_page(request):
	if not request.user.is_authenticated():
		return render(request, 'registration/main_page.html')
	else:
		return HttpResponseRedirect(reverse('deck_choice'))

def login_view(request):
	username = request.POST["e-mail"]
	password = request.POST["password"]
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(reverse('deck_choice'))
		else:
			messages.add_message(request, messagesI.NFO, 'Ваш аккаунт в черном списке') 
	else:
		messages.add_message(request, messages.INFO, 'Неправильный email или пароль') 
	return HttpResponseRedirect(reverse('main_page'))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('main_page'))

def registration_view(request):
	if request.method == "POST":
		username = request.POST["e-mail"]
		password = request.POST["password"]
		user = User(username=username)
		user.save()
		user.set_password(password)
		user.save()
		return HttpResponse('OK')
	else:
		return render(request, 'registration/registration.html')