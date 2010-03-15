from django.template import Context, loader,RequestContext
from django.http import HttpResponse,HttpResponseRedirect

from hey.users.sinaRead import SinaRead
from hey.users.forms import UserForm,UserMoreInfoForm,UserCreationForm,LoginForm
from hey.users.models import User,UserMoreInfo,Message
from django.shortcuts import render_to_response,get_object_or_404

from django.core.context_processors import csrf
from django.template.context import RequestContext
import django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from hey.decorators import myuser_login_required
from hey.decorators import myuser_login_required
from django.core.urlresolvers import reverse

@myuser_login_required
def index(request):
    c = {}
    return render_to_response('index.html', c)

@myuser_login_required
def my(request):
    user_id = request.session['user_id']
    user = get_object_or_404(User, pk=user_id)
    userMoreInfo = UserMoreInfo.objects.filter(user_id=user_id)
    messages = Message.objects.all().order_by('-id')[:5]
    recomms = User.objects.all()[:4]

    c = RequestContext(request,{
    'user_id':user_id,
    'myself':user,
    'userMoreInfo':userMoreInfo,
    'recomms':recomms,
    'messages': messages,
    })
    return render_to_response('my.html', c)

def xhr_test(request):
    if request.is_ajax():
        message = "Hey001.com"
    else:
        message = "Hello"
    return HttpResponse(message)

def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("view",args=(user.id,)))

        else:
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
        moreform = UserMoreInfoForm()
        c = {
        'form':form,
        'moreform': moreform
        }
        c.update(csrf(request))

    return render_to_response('reg.html', c)

def login(request):
    if request.method == 'POST':
        u = User.objects.get(username = request.POST['username'])
      
        if u.validate_password(request.POST['password']):
            request.session['user_id'] = u.id
            return HttpResponseRedirect(reverse("my",args=()))
        else:
            loginForm = LoginForm()
            c = RequestContext(request,{
            'loginForm': loginForm,
            'validate_message':'wrong password'
            })
        return render_to_response('login.html',c)
    else:
        loginForm = LoginForm()
        c = RequestContext(request,{
        'loginForm': loginForm
        })
        return render_to_response('login.html',c)

@myuser_login_required
def logout(request):
    try:
        del request.session['user_id']
    except KyeError:
        pass
    return HttpResponse('You are loged out.')

@myuser_login_required
def fillmore(request):
    session_user_id = request.session['user_id']
    if session_user_id:
        if request.method == 'POST':
            form = UserMoreInfoForm(request.POST)
            if form.is_valid():
                userMoreInfo = form.save(session_user_id)
                return HttpResponseRedirect(reverse("my",args=()))
            else:
                return HttpResponseRedirect('/')
        else:
            moreform = UserMoreInfoForm()
            c = RequestContext(request,{
            'moreform': moreform
            })

        return render_to_response('fillmore.html', c)
    else:
        return HttpResponse('Please Login First')

def view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    userMoreInfo = UserMoreInfo.objects.filter(user_id=user_id)
    c = {
    'user':user,
    'userMoreInfo': userMoreInfo
    }
    return render_to_response('view.html', c)

@myuser_login_required
def editself(request):
    user_id = request.session["user_id"]
    if user_id:
        return edit(request,user_id)

@myuser_login_required
def edit(request, user_id):
    if not checkPrivilege(user_id,request):
        return HttpResponse('not yourself')
    else:
        user = get_object_or_404(User, pk=user_id)
        try:
            userMoreInfo = UserMoreInfo.objects.get(pk=user)
        except UserMoreInfo.DoesNotExist:
            userMoreInfo = UserMoreInfo(user_id=user)
            userMoreInfo.save()
        if request.method == 'POST':
            form = UserForm(request.POST, instance = user)
            print form.is_valid()
            print form.toString()
            if form.is_valid():
                user = form.save()
                return HttpResponseRedirect(reverse("my",args=()))
            else:
                return HttpResponseRedirect(reverse("reg",args=()))
        else:
            form = UserForm(instance = user)
            if userMoreInfo:
                userMoreInfoForm = UserMoreInfoForm(instance = userMoreInfo)
            else:
                userMoreInfoForm = UserMoreInfoForm()
            c = RequestContext(request,{
            'form':form,
            'user_id':user_id,
            'moreform': userMoreInfoForm,
            })

            return render_to_response('edit.html', c)

@myuser_login_required
def addInfo(request,user_id):
    if not checkPrivilege(user_id,request):
        return HttpResponse('not yourself')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                return HttpResponseRedirect(reverse("my",args=()))
            else:
                return HttpResponseRedirect('/')
        else:
            form = UserForm()
            c = RequestContext(request,{'form':form})
    return render_to_response('addinfo.html', c)

def find(request):
    return django.http.HttpResponseForbidden



#
#check session user is user self
#
def checkPrivilege(user_id,request):
    session_user_id = int(request.session['user_id'])
    user_id = int(user_id)
    if user_id == session_user_id:
        return True
    else:
        return False
