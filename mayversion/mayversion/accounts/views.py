from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Message
from accounts.models import UserProfile,UserMoreProfile,WhoVisitMe,listWhoVisitMe
from accounts.forms import UserProfileForm,UserMoreProfileForm
from datings.models import Dating
from microblog.models import TweetInstance,Following
from django.contrib.contenttypes.models import ContentType
from microblog.forms import TweetForm
from votes.models import Poll
# from polls.models import Poll
from photologue.models import Photo

def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            return HttpResponseRedirect(reverse("my",args=()))
        else:
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('regist.html', locals())


@login_required
def my(request):
    user = request.user
    user_profile = user.profile
    
    #will be filter by user self
    messages = Message.objects.all().order_by('-id')[:5]
    datings = Dating.objects.all().order_by('-id')[:5]
    recomms = User.objects.all().order_by('-id')[:4]
    tweets = TweetInstance.objects.tweets_for(request.user)[:10]
    
    # votes = Poll.objects.all().order_by('-id')[:4]
    #   photos = Photo.objects.all().order_by('-id')[:4]
    #   
    votes = Poll.objects.filter(owner=user).order_by('-id')[:4]
    photos = Photo.objects.filter(user=user).order_by('-id')[:4]
    
    
    following = Following.objects.filter(follower_object_id=user.id,
                                            follower_content_type=ContentType.objects.get_for_model(user))
    following_list = [u.followed_content_object for u in following]
    
    followers = Following.objects.filter(followed_object_id=user.id,
                                               followed_content_type=ContentType.objects.get_for_model(user))
    followers_list = [u.follower_content_object for u in followers]
    
    
    try:
        visitors = listWhoVisitMe(user)
    except WhoVisitMe.DoesNotExist:
        print 'Does Not Exist'
        visitors = []        
    return render_to_response('main.html', locals())

@login_required
def space(request,user_id):
    user = request.user
    visit_user = get_object_or_404(User,pk = user_id)
    WhoVisitMe(master = visit_user, visitor = user).save()
    tweets = TweetInstance.objects.tweets_for(request.user)[:10]
    
    votes = Poll.objects.filter(owner=visit_user).order_by('-id')[:4]
    photos = Photo.objects.filter(user=visit_user).order_by('-id')[:4]
    
    following = Following.objects.filter(follower_object_id=visit_user.id,
                                            follower_content_type=ContentType.objects.get_for_model(visit_user))
    following_list = [u.followed_content_object for u in following]
    
    followers = Following.objects.filter(followed_object_id=visit_user.id,
                                               followed_content_type=ContentType.objects.get_for_model(visit_user))
    followers_list = [u.follower_content_object for u in followers]
    
    
    try:
        visitors = listWhoVisitMe(visit_user)
    except WhoVisitMe.DoesNotExist:
        print 'Does Not Exist'
        visitors = []
        
    
    visitorfollowing = Following.objects.filter(follower_object_id=user.id,
                                              follower_content_type=ContentType.objects.get_for_model(user),
                                        followed_object_id=visit_user.id,
                                            followed_content_type=ContentType.objects.get_for_model(visit_user)
                                              )
    if(len(visitorfollowing.all()) == 1):
        follow_relative = True
    else:
        follow_relative = False
    
    
    return render_to_response('space.html',locals())


@login_required
def edit(request):
    user = request.user
    try:
        userProfile = UserProfile.objects.get(user = user)
    except UserProfile.DoesNotExist:
        userProfile = UserProfile(user = user)
        userProfile.save()

    userProfileForm = UserProfileForm(instance = userProfile)

    if request.method == 'POST':
        userProfileForm = UserProfileForm(request.POST, instance = userProfile)

        if userProfileForm.is_valid():
            userProfile = userProfileForm.save(user.id)
            return HttpResponseRedirect(reverse("my",args=()))
        else:
            return HttpResponseRedirect(reverse("edit",args=()))

    else:
        userProfileForm = UserProfileForm(instance = userProfile)

        return render_to_response('edit.html',locals())


@login_required
def editMore(request):
    user = request.user
    try:
        userMoreProfile = UserMoreProfile.objects.get(user = user.profile)
    except UserMoreProfile.DoesNotExist:
        userMoreProfile = UserMoreProfile(user = user.profile)
        userMoreProfile.save()

    userMoreProfileForm = UserMoreProfileForm(instance = userMoreProfile)

    if request.method == 'POST':
        userMoreProfileForm = UserMoreProfileForm(request.POST, instance = userMoreProfile)

        if userMoreProfileForm.is_valid():
            userMoreProfile = userMoreProfileForm.save(user.profile.id)
            return HttpResponseRedirect(reverse("my",args=()))
        else:
            return HttpResponseRedirect(reverse("editMore",args=()))

    else:
        userMoreProfileForm = UserMoreProfileForm(instance = userMoreProfile)
        return render_to_response('editMore.html',locals())




def search(request):
    user = request.user



def friends(request):
    return HttpResponse('''
    @peter \n
    @yanger \n
    @caoxg \n
    @ydtang \n
    @gzx \n
    @kcome \n
    ''')