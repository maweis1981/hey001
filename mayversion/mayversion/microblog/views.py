#!/usr/bin/env python
# encoding: utf-8


from django.shortcuts import render_to_response, get_object_or_404,HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from microblog.models import Tweet, TweetInstance, Following
from microblog.forms import TweetForm

from django.utils import simplejson




from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@login_required
def personal(request):
    if request.method == "POST":
        form = TweetForm(request.user, request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            form.save()

            if success_url is None:
                success_url = reverse('microblog.views.personal')
            return HttpResponseRedirect(success_url)
        reply = None
    else:
        reply = request.GET.get("reply", None)
        form = TweetForm()
        if reply:
            form.fields['text'].initial = u"@%s " % reply
    user = request.user
    tweets = TweetInstance.objects.tweets_for(request.user)
    return render_to_response('microblog/personal.html',locals())

@login_required
def ajaxTweetSend(request):
    print request.user
    print request.POST
    try:
        form = TweetForm(request.user, request.POST)
    except (RuntimeError, TypeError, NameError):
        pass
    print form.is_valid()
    if form.is_valid():
        form.save()
        return HttpResponse('{result:ok}')
    else:
        return HttpResponse('{result:data error}')

    #        reply = None
    #    else:
    #        reply = request.GET.get("reply", None)
    #        form = TweetForm()
    #        if reply:
    #            form.fields['text'].initial = u"@%s " % replhgy µi nhy
    #    tweets = TweetInstance.objects.tweets_for(request.user).order_by("-sent")

@login_required
def ajaxTweetList(request):
    tweets = TweetInstance.objects.tweets_for(request.user)
    tw_lists = []
    for t in tweets:
        tw_lists.append(
                {
                 'user_id': t.sender_id,   
                 'name': t.sender.username,
                 'text': t.text,
                 'sent': str(t.sent),
                }
                )
    return JsonResponse(tw_lists)

@login_required
def ajaxPublicTweetList(request):
    tweets = TweetInstance.objects.public_tweets()
    tw_lists = []
    for t in tweets:
        tw_lists.append(
                {
                 'user_id': t.sender_id,
                 'name': t.sender.__unicode__(),
                 'text': t.text,
                 'sent': str(t.sent),
                }
                )
    return JsonResponse(tw_lists)


def public(request, template_name="microblog/public.html"):
    """
    all the tweets
    """
    tweets = Tweet.objects.all().order_by("-sent")

    return render_to_response(template_name, {
    "tweets": tweets,
    }, context_instance=RequestContext(request))

def single(request, id, template_name="microblog/single.html"):
    """
    A single tweet.
    """
    tweet = get_object_or_404(Tweet, id=id)
    return render_to_response(template_name, {
    "tweet": tweet,
    }, context_instance=RequestContext(request))


def _follow_list(request, other_user, follow_list, template_name):
# the only difference between followers/following views is template
# this function captures the similarity

    return render_to_response(template_name, {
    "other_user": other_user,
    "follow_list": follow_list,
    }, context_instance=RequestContext(request))

def followers(request, username, template_name="microblog/followers.html"):
    """
    a list of users following the given user.
    """
    other_user = get_object_or_404(User, username=username)
    users_followers = Following.objects.filter(followed_object_id=other_user.id,
                                               followed_content_type=ContentType.objects.get_for_model(other_user))
    follow_list = [u.follower_content_object for u in users_followers]
    return _follow_list(request, other_user, follow_list, template_name)

def following(request, username, template_name="microblog/following.html"):
    """
    a list of users the given user is following.
    """
    other_user = get_object_or_404(User, username=username)
    following = Following.objects.filter(follower_object_id=other_user.id,
                                         follower_content_type=ContentType.objects.get_for_model(other_user))
    follow_list = [u.followed_content_object for u in following]
    return _follow_list(request, other_user, follow_list, template_name)

def toggle_follow(request, username):
    """
    Either follow or unfollow a user.
    """
    other_user = get_object_or_404(User, username=username)
    if request.user == other_user:
        is_me = True
    else:
        is_me = False
    if request.user.is_authenticated() and request.method == "POST" and not is_me:
        if request.POST["action"] == "follow":
            Following.objects.follow(request.user, other_user)
            request.user.message_set.create(
                    message=_("You are now following %(other_user)s") % {'other_user': other_user})
            if notification:
                notification.send([other_user], "tweet_follow", {"user": request.user})
        elif request.POST["action"] == "unfollow":
            Following.objects.unfollow(request.user, other_user)
            request.user.message_set.create(
                    message=_("You have stopped following %(other_user)s") % {'other_user': other_user})
    return HttpResponseRedirect(reverse("my"))




class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
            print content
        else:
            content = simplejson.dumps(object, indent=2, cls=HeyEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')

class HeyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        print obj
        if isinstance(obj, TweetInstance):
            print '---------'
            return [obj.text,obj.sent,obj.sender.name]
        return simplejson.JSONEncoder.default(self, obj)
        