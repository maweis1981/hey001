from django.template import  Context,loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from hey.users.models import User
from hey.messages.forms import MessageForm
from django.core.context_processors import csrf
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse

def send(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            print message.content
            return HttpResponseRedirect(reverse("message_success"))
        else:
            return HttpResponseRedirect('/')
    else:
        form = MessageForm()
        c = RequestContext(request,{'form':form})
        return render_to_response('messages/send.html', c)

def myTransferMessages(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    sendMessages = user.send_messages
    receiveMessages = user.receive_messages
    c = RequestContext(request,{
        'send_messages':sendMessages,
        'receive_messages':receiveMessages,
    })
    return render_to_response('messages/my.html', c)


def success(request):
    c = RequestContext(request,{})
    return render_to_response('messages/success.html', c)