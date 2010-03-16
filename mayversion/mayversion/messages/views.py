from django.template import  Context,loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from mayversion.messages.forms import MessageForm
from mayversion.messages.models import Message

@login_required
def send(request):
    user = request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            print message.content
            return HttpResponseRedirect(reverse("message_success"))
        else:
            return HttpResponseRedirect(reverse("my"))
    else:
        form = MessageForm()
        return render_to_response('messages/send.html', locals())

@login_required
def sendToUser(request,user_id):
    user = request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            print message.content
            return HttpResponseRedirect(reverse("message_success"))
        else:
            return HttpResponseRedirect(reverse("my"))
    else:
        message = Message(receiver = User.objects.get(pk = user_id))
        form = MessageForm(instance = message)        
        return render_to_response('messages/send.html', locals())

@login_required
def myMessages(request):
    user = get_object_or_404(User, pk=request.user.id)
    send_messages = user.send_messages
    receive_messages = user.receive_messages
    
    return render_to_response('messages/my.html', locals())

@login_required
def success(request):
    user = request.user
    return render_to_response('messages/success.html', locals())