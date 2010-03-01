from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect

from hey.users.sinaRead import SinaRead
from hey.users.forms import UserForm,User
from django.shortcuts import render_to_response,get_object_or_404

from django.core.context_processors import csrf



def index(request):
    c = {}
    return render_to_response('index.html', c)


def my(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    recomms = User.objects.all()[:4]

    c = {
    'user_id':user_id,
    'user':user,
    'recomms':recomms,
    }
    return render_to_response('my.html', c)


def xhr_test(request):
    if request.is_ajax():
        message = "Hey001.com"
    else:
        message = "Hello"
    return HttpResponse(message)

def reg(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print user.id
            forward_url = '/user/my/' + str(user.id)
            print forward_url
            return HttpResponseRedirect(forward_url)
        else:
            return HttpResponseRedirect('/')
    else:
        form = UserForm()

        c = {'form':form}
        c.update(csrf(request))

    return render_to_response('reg.html', c)



def view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    c = {'user':user}
    return render_to_response('view.html', c)

def edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            user = form.save()
            print user.id
            forward_url = '/user/my/' + str(user.id)
            print forward_url
            return HttpResponseRedirect(forward_url)
        else:
            return HttpResponseRedirect('/user/reg')
    else:
        form = UserForm(instance = user)
        c = {'form':form,'user_id':user_id}
        c.update(csrf(request))
        return render_to_response('edit.html', c)

        
def addInfo(request,user_id):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print user.id
            forward_url = '/user/my/' + str(user.id)
            print forward_url
            return HttpResponseRedirect(forward_url)
        else:
            return HttpResponseRedirect('/')
    else:
        form = UserForm()

        c = {'form':form}
        c.update(csrf(request))

    return render_to_response('addinfo.html', c)

