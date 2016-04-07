import json
import uuid

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from .models import UserProfile, Friendship, PendingMessage, MessagePool


def home(request):
    return render(request, 'basic/homepage.html')


@csrf_exempt
def user_login(request):
    if request.method == 'POST' and not request.user.is_authenticated():
        device = request.POST['device']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if device == 'mobile':
                    name = user.first_name + ' ' + user.last_name
                    phone = user.username
                    email = user.email
                    user_dict = {'name': name, 'phoneno': phone, 'email': email}
                    success = {'error': '0', 'error_msg': 'Login Successful', 'user': user_dict}
                    return HttpResponse(json.dumps(success), content_type="application/json")
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Account is disabled.")
        else:
            if device == 'mobile':
                if not User.objects.filter(username=username).exists():
                    error = {'error': '2', 'error_msg': 'User not found'}
                else:
                    error = {'error': '1', 'error_msg': 'Invalid credentials'}
                return HttpResponse(json.dumps(error), content_type="application/json")
            print "Invalid login details: {0}, 	{1}".format(username, password)

    return render(request, 'basic/login.html', {'display': True})


@csrf_exempt
def search(request):
    if request.method == 'POST':
        try:
            phone = request.POST['username']
            if User.objects.filter(username=phone).exists():
                user = User.objects.get(username=phone)
                name = user.first_name + ' ' + user.last_name
                phone = user.username
                email = user.email
                user_dict = {'name': name, 'phoneno': phone, 'email': email}
                success = {'error': '0', 'user': user_dict}
                return HttpResponse(json.dumps(success), content_type="application/json")
            else:
                error = {'error': '1', 'error_msg': 'Username not found'}
                return HttpResponse(json.dumps(error), content_type="application/json")
        except:
            pass


def get_user_profile(user):
    if UserProfile.objects.filter(user=user).exists():
        return UserProfile.objects.get(user=user)


@csrf_exempt
def add_friend(request):
    if request.method == 'POST':
        try:
            person_username = request.POST['username']
            friend_username = request.POST['friendusername']
            person = User.objects.get(username=person_username)
            friend = User.objects.get(username=friend_username)
            Friendship(person=get_user_profile(person), friend=get_user_profile(friend)).save()
            name = friend.first_name + ' ' + friend.last_name
            phone = friend.username
            email = friend.email
            user_dict = {'name': name, 'phoneno': phone, 'email': email}
            success = {'error': '0', 'friend': user_dict}
            return HttpResponse(json.dumps(success), content_type="application/json")

        except:
            pass


@csrf_exempt
def register(request):
    context = {}
    if request.method == 'POST':
        try:  # handling bad POST packets

            context['label'] = True
            context['type'] = 'danger'

            device = request.POST['device']
            email = request.POST['email']
            password = request.POST['password']

            if device == 'mobile':
                name = request.POST['name']
                fname = name.split(' ')[0]
                lname = name[len(fname)-1:]
                phone = request.POST['phoneno']
            else:
                fname = request.POST['fname']
                lname = request.POST['lname']
                phone = request.POST['phone']

            if User.objects.filter(username=phone).exists():
                context['email'] = email
                context['fname'] = fname
                context['lname'] = lname
                context['not_unique'] = True
                if device == 'mobile':
                    error = {'error': '1', 'error_msg': 'Mobile already exists'}
                    return HttpResponse(json.dumps(error), content_type="application/json")
                return render(request, 'basic/register.html', context)

            user = User.objects.create_user(email=email, first_name=fname, last_name=lname,
                                            username=phone, password=password)
            UserProfile(user=user, phone=phone).save()
            context['type'] = 'success'
            context['message'] = 'Registration Successful. You can now login!!!!'
            context['tag'] = 'Congratulations!'
            if device == 'mobile':
                success = {'error': '0', 'error_msg': 'Registration Complete'}
                return HttpResponse(json.dumps(success), content_type="application/json")
            if request.user.is_authenticated():
                logout(request)
            return render(request, 'basic/homepage.html', context)

        except:
            return HttpResponseRedirect('/')  # bad POST

    # redirecting to step 2

    else:
        return render(request, 'basic/register.html', context)  # redirecting to step 2


@csrf_exempt
def message_aa_gaya(request):
    if request.method == 'POST':

        message = request.POST['message']
        source = request.POST['source']
        message_type = request.POST['type']
        data_string = request.POST['string']
        print 'message: ' + message
        ids = data_string.split(',')
        print ids
        source_profile = UserProfile.objects.get(phone=source)

        messageObj = PendingMessage(source=source_profile, message=message, message_type=message_type)
        messageObj.save()
        print messageObj
        for id in ids:
            user_profile = UserProfile.objects.get(phone=id)
            MessagePool(person=user_profile, message=messageObj).save()

        success = {'error': '0', 'error_msg': 'Successfully sent hangout invitations on you behalf Sir'}
        return HttpResponse(json.dumps(success), content_type="application/json")


@csrf_exempt
def check_message(request):
    if request.method == 'POST':
        source = request.POST['source']
        message_type = request.POST['type']
        user = UserProfile.objects.get(phone=source)
        if user.pending_messages.all().filter(message_type=message_type).exists():
            messageBundle = user.pending_messages.all().filter(message_type=message_type).first()
            pool = MessagePool.objects.get(message=messageBundle)
            message = messageBundle.message
            source = messageBundle.source

            source_user = source.user

            name = source_user.first_name + ' ' + source_user.last_name
            phone = source_user.username
            email = source_user.email
            user_dict = {'name': name, 'phoneno': phone, 'email': email}

            message = {'message': message, 'source': user_dict}
            pool.delete()

            success = {'error': '0', 'error_msg': 'Successful', 'message': message}
            return HttpResponse(json.dumps(success), content_type="application/json")

        else:
            error = {'error': '1', 'error_msg': 'No messages'}
            return HttpResponse(json.dumps(error), content_type="application/json")






