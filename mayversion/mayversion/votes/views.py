#!/usr/bin/env python
# encoding: utf-8
from django.forms.models import inlineformset_factory
from votes.models import Poll,Choice,Vote
from votes.forms import PollForm, PollFormset,get_polledititem_formset, ChoiceForm,ChoiceFormset,get_vote_formset
from django.shortcuts import render_to_response,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.models import User,Message
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def display_data(request, data, **kwargs):
    return render_to_response('votes/posted-data.html', dict(data=data, **kwargs),
        context_instance=RequestContext(request))

def newPoll(request, form_class, template):
    PollFormset = get_polledititem_formset(form_class, extra=4)
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            p = form.save()
            print type(p)
            formset = PollFormset(request.POST,instance=p)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect('/votes/vote/%s'% p.id)
    else:
        form = PollForm()
        formset = PollFormset()
    return render_to_response(template, {'form': form, 'formset': formset, 'request':request,},
        context_instance=RequestContext(request))
        
                
def vote(request,vote_id):
    if request.method == 'POST':
        poll_id = request.POST['poll_id']
        print 'Poll Id is %s ' % poll_id
        vote = request.POST.getlist('vote')
        print 'votes [ %s ]' % vote
        u = request.user
        print u
        if not u:
            u = User.objects.get(pk = 1)
            
        p = Poll.objects.get(pk = poll_id)
        for v in vote:
            c = Choice.objects.get(pk = v)
            vote = Vote(poll = p ,user = u, choice = c)
            check_vote = Vote.objects.filter(poll = p ,user = u, choice = c)
            if not check_vote:
                vote.save()
            else:
                return render_to_response('votes/vote.html', {'poll': p,  'request':request,'msg': 'Already Vote This Poll.'},context_instance=RequestContext(request))
    else:
        pass
    poll = get_object_or_404(Poll, pk = vote_id)
    return render_to_response('votes/vote.html', { 'request':request,'poll': poll},context_instance=RequestContext(request))

    
    
    
def listVotes(request):
    polls = Poll.objects.all()
    paginator = Paginator(polls, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except valueError:
        page = 1

    try:
        polls = paginator.page(page)
    except (EmptyPage, InvalidPage):
        polls = paginator.page(paginator.num_pages)

    return render_to_response('votes/list.html', { 'request':request,'polls': polls},context_instance=RequestContext(request))