# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt



from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.template import Context, loader

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required



def index(request):
    return render_to_response('index.html',{})

def createuser_prompt(request):
    return render_to_response('createuser.html',{})

def createuser(request):
    
    username = request.POST['username']
    email = request.POST['e-mail']
    password = request.POST['password']

    
    user = User.objects.create_user(username,email,password)
    user.save()
    
        
    t = loader.get_template('login.html') 
    c = Context({
        'username' : username,
    })
    
    return HttpResponse(t.render(c))
        


    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    #return HttpResponseRedirect('/polls/%s/results/' % p.id)
    
    #if not successful:
    #return render_to_response('createuser.html',{})

def login_prompt(request):
    return render_to_response('login.html',{})

def loginuser(request):


    #return render_to_response('mainmenu.html',{})
    username = request.POST['username']
    password =  request.POST['password']
    user = authenticate(username=username,password=password)

    #return HttpResponse(simplejson.dumps({'success': True}))
    
    if user is not None:
        #if user.is_active:
        login(request,user)
        return HttpResponse(simplejson.dumps({'success': True}))
        #else:
        #       return HttpResponse(simplejson.dumps({'success': False, 'errors': { 'reason': 'Your acct has been disabled.'}}))

    else:
        return HttpResponse(simplejson.dumps({'success': False, 'errors': { 'reason': 'Your username or password was incorrect.'}}))

#def authenticate(username,password):
#    if username in ['scott'] and password in [';lkjJK']:
#        return True
#    else:
#        return None


def logout_view(request):
    logout(request)
    return render_to_response('logout.html',{})




def failure(request):
    return HttpResponse('no, failure')  

def mainmenu(request):
    if not request.user.is_authenticated():
        return render_to_response('login_redirect.html',{})
        #return HttpResponse('You are not logged in. Please login here.')
    
    else:
        t = loader.get_template('mainmenu.html') 
        c = Context({
            'name' : 'Scott',
        })
        return HttpResponse(t.render(c))
        #return render_to_response('mainmenu.html',{})
        #return HttpResponse('You ARE logged in')

@login_required
def test(request):
    #return HttpResponse('ok')
    return render_to_response('login_redirect.html',{})


def lingdesktop(request):
    return render_to_response('lingdesktop.html',{})


