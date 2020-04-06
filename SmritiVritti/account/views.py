from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from .forms import  AddUserForm as userform
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
import requests
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from . custom_decorator import *
	
# Create your views here.
def registration(request,templates='account/registration.html'):
	
	if request.method == "POST":
		form = userform(request.POST)
		print('hellwejqerhoto')
		
		if form.is_valid():
			user=form.save(commit=False)
			user.is_active = False
			user.save()
			email_or_phone = form.cleaned_data.get('username')
			if '@' in email_or_phone:
				

				current_site = get_current_site(request)
				mail_subject = 'Activate your blog account.'
				message = render_to_string('account/acc_active_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
					})
				to_email = form.cleaned_data.get('username')
				email = EmailMessage(
						mail_subject, message, to=[to_email]
				)
				print(email.send())
				return HttpResponse('Please confirm your email address to complete the registration')
			else:
				#https://2factor.in/API/V1/{api_key}/SMS/+91{user's_phone_no}/AUTOGEN
				#{ "Status": "Success", "Details": "5D6EBEE6-EC04-4776-846D"}
					api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'
				#try:
					phone_no = '+91' + email_or_phone
					message = None
					print(phone_no)
					status = requests.post("https://2factor.in/API/V1/"+api_key+"/SMS/"+phone_no+"/AUTOGEN",data={})
					status = status.json()
					print(type(status),status)
					request.session['session_id'] = status.get("Details")
					print(request.session)
					if status.get('Status') == "Success":
						print(status)
						message = "enter otp"
						request.user = email_or_phone
						request.session['pk'] = user.pk 
						print(status)
					print(status)
					return render(request,'account/checkOtp.html',{'message':message})

				#except Exception as e:
					#return HttpResponse('Please enter valid   number to complete the registration')
				
			#email_or_phone=form.cleaned_data.get('username')
			#password=form.cleaned_data.get('password1')
			#user=authenticate(email_or_phone,password=password)
			#if user and user.is_active:
				#print('hello')
				#login(request, user)
				#return render(request,templates,{'form':form,'error':'user created'})

				
		else:
			form = userform()
			return render(request,templates,{'form':form,'error':'user allready exist '})




		


	else:
		form = userform()
		return render(request,templates,{'form':form,})
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		#login(request, user)
		# return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		user.delete()

		return HttpResponse('Activation link is invalid!')
def conform_otp(request):
	if request.method == 'POST':
		#https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_entered_by_user}
		api_key = 'c1003ac3-a97d-11e9-ade6-0200cd936042'

		otp = request.POST.get('otp')
		verify = "https://2factor.in/API/V1/"+api_key+"/SMS/VERIFY/"+request.session.get('session_id')+"/"+otp
		status = requests.post(verify)
		status = status.json()
		user =  User.objects.get(pk=request.session.get('pk'))
		print(status)
		if user and status.get('Status') == 'Success':
			user.is_active = True
			user.save()
			new_group, created = Group.objects.get_or_create(name ='staff')
			user.groups.add(new_group)
			
			

			#login(request, user)
		# return redirect('home')
			return HttpResponse('Thank you for your mobile no is verified. Now you can login your account.')
		else:
			user.delete()
			return HttpResponse('Activation link is invalid!')


def Login(request,templates='account/registration.html'):
	if request.method == 'POST':

		email_or_phone = request.POST.get('email_or_phone')
		password = request.POST.get('password')
		print('hello')
		user =  authenticate(username=email_or_phone,password = password)
		print('hello')
		print(user.is_active)
		#@group_required('level0')
		print(user)
		if user  and user.is_active :

			try:
				login(request, user)
				print('hello')
				return HttpResponse('user login sucessfully')
			except e:
				return HttpResponse('user can not sucessfully')

	
		return HttpResponse('user not exist')
	else:
		return render(request,templates,{'form':None})
@group_required('staff')
def d(request):
	return HttpResponse('welocme')

	
