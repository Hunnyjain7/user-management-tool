import random
import re
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import UsrUser, UsrGender
from django.contrib import messages


class Register(View):
    def get(self, request):
        try:
            if 'id' in request.session:
                return redirect('homepage')
            else:
                gender = UsrGender.objects.all()
                return render(request, 'register.html', {"context": gender})
        except Exception as e:
            print(e)
            return redirect('login')

    def post(self, request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            mobile_no = request.POST.get('mobile_no')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            profile_image = request.FILES.get('profile_image')
            designation = request.POST.get('designation')
            print(first_name
                  , last_name
                  , username
                  , email
                  , gender
                  , mobile_no
                  , password
                  , confirm_password,
                  profile_image, designation)

            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_check = UsrUser.objects.filter(email=email).exists()
            mobile_check = UsrUser.objects.filter(mobile_no=int(mobile_no)).exists()
            username_check = UsrUser.objects.filter(username=username).exists()
            error_message = None
            if not first_name or first_name == '':
                error_message = 'First Name is Required !!'
            elif not last_name or last_name == '':
                error_message = 'Last Name is Required !!'
            elif not username or username == '':
                error_message = 'Username is Required !!'
            elif not email or email == '':
                error_message = 'Email is Required !!'
            elif not gender or gender == '':
                error_message = 'Gender is Required !!'
            elif not mobile_no or mobile_no == '':
                error_message = 'Mobile number is Required !!'
            elif not password or password == '':
                error_message = 'Password is Required !!'
            elif not confirm_password or confirm_password == '':
                error_message = 'Confirm Password is Required !!'
            elif not designation or designation == '':
                error_message = 'Designation is Required !!'
            elif not re.fullmatch(email_regex, email):
                error_message = 'Invalid Email !!'
            elif len(str(mobile_no)) != 10:
                error_message = 'Mobile number must be of 10 digits !!'
            elif password != confirm_password:
                error_message = 'Password Miss match !!'
            elif len(password) < 6:
                error_message = 'Password length must be greater than 5 digits !!'
            elif email_check:
                error_message = 'Email already exists !!'
            elif mobile_check:
                error_message = 'Mobile Number already exists !!'
            elif username_check:
                error_message = 'Username already exists !!'
            if not error_message:
                user_code = 'USR' + str(random.randint(9999, 9999999))
                gender_obj = UsrGender.objects.get(id=gender)
                profile = UsrUser(
                    first_name=first_name, last_name=last_name, username=username, email=email, user_code=user_code,
                    gender=gender_obj, mobile_no=int(mobile_no), password=password,
                    profile_image=profile_image, designation=designation
                )
                profile.save()
                messages.success(request, "Registration Successful")
                return JsonResponse({"status_code": 200, "message": "Registration Successful"})
            else:
                return JsonResponse({"status_code": 402, "message": error_message})
        except Exception as e:
            print(e)
            return redirect('register')


class LogIn(View):
    def get(self, request):
        try:
            if 'id' in request.session:
                return redirect('homepage')
            else:
                return render(request, 'login.html')
        except Exception as e:
            print(e)
            return redirect('login')

    def post(self, request):
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = UsrUser.objects.filter(email=email).filter(password=password)
            if user.exists():
                request.session['id'] = user[0].id
                messages.success(request, "Logged in Successfully")
                return JsonResponse({"status_code": 200, "message": "Logged in Successfully"})
            else:
                return JsonResponse({"status_code": 402, "message": "Invalid Credential's"})
        except Exception as e:
            print(e)
            return redirect('login')


class Home(View):
    def get(self, request):
        try:
            if 'id' in request.session:
                return render(request, 'home.html')
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            return redirect('login')


class UpdateProfile(View):
    def get(self, request):
        try:
            if 'id' in request.session:
                gender = UsrGender.objects.all()
                user = UsrUser.objects.get(id=request.session['id'])
                return render(request, 'profile.html', {"user": user, "context": gender})
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            return redirect('login')

    def post(self, request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            mobile_no = request.POST.get('mobile_no')
            designation = request.POST.get('designation')
            user = UsrUser.objects.get(id=request.session['id'])

            error_message = None
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if user.email != email:
                email_check = UsrUser.objects.filter(email=email).exists()
                if email_check:
                    error_message = 'Email already exists !!'
            if user.mobile_no != mobile_no:
                mobile_check = UsrUser.objects.filter(mobile_no=int(mobile_no)).exists()
                if mobile_check:
                    error_message = 'Mobile Number already exists !!'
            if user.username != username:
                username_check = UsrUser.objects.filter(username=username).exists()
                if username_check:
                    error_message = 'Username already exists !!'
            if not first_name or first_name == '':
                error_message = 'First Name is Required !!'
            elif not last_name or last_name == '':
                error_message = 'Last Name is Required !!'
            elif not username or username == '':
                error_message = 'Username is Required !!'
            elif not email or email == '':
                error_message = 'Email is Required !!'
            elif not gender or gender == '':
                error_message = 'Gender is Required !!'
            elif not mobile_no or mobile_no == '':
                error_message = 'Mobile number is Required !!'
            elif not designation or designation == '':
                error_message = 'Designation is Required !!'
            elif not re.fullmatch(email_regex, email):
                error_message = 'Invalid Email !!'
            elif len(str(mobile_no)) != 10:
                error_message = 'Mobile number must be of 10 digits !!'

            if not error_message:
                gender_obj = UsrGender.objects.get(id=gender)
                profile = UsrUser(
                    id=user.id, first_name=first_name, last_name=last_name, username=username, email=email,
                    gender=gender_obj, mobile_no=int(mobile_no), password=user.password, user_code=user.user_code,
                    profile_image=user.profile_image, designation=designation
                )
                profile.save()
                return redirect('homepage')
            else:
                messages.error(request, error_message)
                return redirect('profile')

        except Exception as e:
            print(e)
            return redirect('update')


def logout(request):
    try:
        request.session.clear()
        return redirect('login')
    except Exception as e:
        print(e)
        return redirect('login')


def delete(request):
    try:
        if 'id' in request.session:
            user = UsrUser.objects.get(id=request.session['id'])
            request.session.clear()
            user.delete()
            return redirect('register')
        else:
            return redirect('login')
    except Exception as e:
        print(e)
        return redirect('login')
