from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import *
from tutorial.outlookservice import get_me, get_my_messages, get_my_events, get_my_contacts


def home(request):
    # redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    redirect_uri = 'http://localhost:8000/tutorial/gettoken/'   # redirect_uri in Azure doesn't take 'http://127.0.0.1' so explicitly changed to 'http://localhost'
    sign_in_url = get_signin_url(redirect_uri)
    context = {
        'sign_in_url': sign_in_url
    }
    template = 'tutorial/home.html'
    return render(request, template, context)


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    # user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']

    expiration = int(time.time()) + expires_in - 300

    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    # return HttpResponse('User: {0}, Access token: {1}'.format(user['displayName'], access_token))
    return HttpResponseRedirect(reverse('tutorial:mail'))


def mail(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        messages = get_my_messages(access_token)
        context = {'messages': messages['value']}
        return render(request, 'tutorial/mail.html', context)


def events(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        events = get_my_events(access_token)
        context = {'events': events['value']}
        return render(request, 'tutorial/events.html', context)


def contacts(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        contacts = get_my_contacts(access_token)
        context = {'contacts': contacts['value']}
        return render(request, 'tutorial/contacts.html', context)
