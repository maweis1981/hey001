# Create your views here.
from django.contrib.auth.models import User
from groups.models import FriendRequest,Friends,my_friends,my_friends_request
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.core import serializers
from reminds.models import UserDeviceToken

import simplejson as json

def requestFriend(request):
    if request.method == 'POST':
         if request.POST['req_id']:
             user = User.objects.get(pk= request.POST['req_id'])
             recipient = User.objects.get(pk= request.POST['rec_id'])
             message = request.POST["message"]
             #check friend request exist.
             if user == recipient:
                 return HttpResponse("{result:self}")
             beFriendRequestExist = FriendRequest.objects.filter(user=recipient,recipientUser=user)
             if len(beFriendRequestExist) > 0:
                 return HttpResponse('{result:beFriendRequest Exist}')
             exist = FriendRequest.objects.filter(user=user,recipientUser=recipient)
             if len(exist) == 0:
                 fr = FriendRequest(user=user,recipientUser=recipient,message=message)
                 fr.save()
                 return HttpResponse('{result:ok}')
             else:
                 return HttpResponse('{result:exist}')
         else:
             return HttpResponse('{result:noData}')
    return HttpResponse('{result:noPost}')

def searchUser(request,username):
    users = User.objects.filter(username__contains=username).order_by('username')
    return render_to_response('groups/users.html',locals())

def searchFriend(request):
    if request.method == 'POST':
        if request.POST['friend_name']:
            users = User.objects.filter(username__contains=request.POST['friend_name']).order_by('username')
            if len(users) > 0:
                response = HttpResponse(mimetype="text/javascript")
                serializers.serialize("json", users, stream=response)
                return response
            else:
                return HttpResponse('{result:not found}')
        else:
            return HttpResonse('{result:could not get friend name}')
    return HttpResponse('{result:not post method request}')

def addFriend(request):
    return render_to_response('groups/addFriend.html',locals())

def requestFriendInWeb(request):
    user = request.user
    if request.method == 'POST':
         if request.POST['rec_id']:
             recipient = User.objects.get(pk= request.POST['rec_id'])
             message = request.POST["message"]
             #check friend request exist.
             if user == recipient:
                 return HttpResponse("{result:self}")
             beFriendRequestExist = FriendRequest.objects.filter(user=recipient,recipientUser=user)
             if len(beFriendRequestExist) > 0:
                 return HttpResponse('{result:beFriendRequest Exist}')
             exist = FriendRequest.objects.filter(user=user,recipientUser=recipient)
             if len(exist) == 0:
                 fr = FriendRequest(user=user,recipientUser=recipient,message=message)
                 fr.save()
                 return HttpResponse('{result:ok}')
             else:
                 return HttpResponse('{result:exist}')
         else:
             return HttpResponse('{result:noData}')
    return HttpResponse('{result:noPost}')


def approveFriendRequest(request):
    print request.method
    print 'approve'
    if request.method == 'POST':
        print 'running post method'
        print request.POST['friend_request_id']
        if request.POST['user_id']:
            print request.POST['user_id']

            user = User.objects.get(pk=request.POST['user_id'])
            print user.username

            friend_request = FriendRequest.objects.get(pk=request.POST['friend_request_id'])
            print friend_request
            if friend_request.recipientUser == user:
                friend = Friends()
                #check friend already exist.
                friend.user = friend_request.user
                friend.friend = user
                friend.friend_request = friend_request
                friend.save()
                print '----'
                friend_request.status = request.POST['friend_request_status']
                print friend_request.status
                friend_request.save()
                print 'friend_request already update'
                return HttpResponse('{result:ok}')
            else:
                return HttpResponse('noPermission')
        return HttpResponse('noUserInfo')
    return HttpResponse('noPOST')

def myRequestFriends(request):
    if request.method == 'POST':
        if request.POST['user_id']:
            user = User.objects.get(pk=request.POST['user_id'])
            requestFriends = my_friends_request(user)
            
            rfs = []
            for rFriend in requestFriends:
                rf = {}
                rf['request_id'] = rFriend.id
                rf['user'] = rFriend.user.username
                rf['user_id'] = rFriend.user.id
                rf['recipienter'] = rFriend.recipientUser.username
                rf['recipienter_id'] = rFriend.recipientUser.id
                rf['message'] = rFriend.message
                rf['status'] = rFriend.status
                rf['date_sent'] = '%s' % rFriend.date_sent
                rfs.append(rf)
            
            return HttpResponse(json.dumps(rfs))
        else:
            return HttpResponse('noData')
    return HttpResponse('noPost')


def myRequestFriendsList(request):
    user = request.user
    requestFriends = my_friends_request(user)
    return render_to_response('groups/requestFriends.html',locals())

def myFriendList(request):
    user = request.user
    friends = my_friends(user)
    return render_to_response('groups/friends.html', locals())
    
    
def myFriends(request):
    if request.method == 'POST':
        if request.POST['user_id']:
            user = User.objects.get(pk=request.POST['user_id'])
            friends = my_friends(user)
#resort user data,
#sort self,friends...
#add devicetoken into obj
            fs = []
            sf = {}
            sf['user'] = user.username
            sf['user_id'] = user.id
            sf['date_created'] = '%s' % user.date_joined
            fs.append(sf)
            for f in friends:
                rf = {}
                if f.user == user:
                    rf['user'] = f.friend.username
                    rf['user_id'] = f.friend.id
                else:
                    rf['user'] = f.user.username
                    rf['user_id'] = f.user.id
                    
                rf['date_created'] = '%s' % f.date_created
                fs.append(rf)
            
            return HttpResponse(json.dumps(fs))

            return response
        else:
            return HttpResponse('noData')
    return HttpResponse('noPost')
