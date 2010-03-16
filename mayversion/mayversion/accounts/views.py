from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Message
from mayversion.accounts.models import UserProfile,UserMoreProfile
from mayversion.accounts.forms import UserProfileForm,UserMoreProfileForm

def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
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
	messages = Message.objects.all().order_by('-id')[:5]
	recomms = User.objects.all()[:4]
	return render_to_response('my.html', locals())


@login_required
def space(request,user_id):
    user = request.user
    visit_user = get_object_or_404(User,pk = user_id)
    visit_user_profile = visit_user.profile
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
    