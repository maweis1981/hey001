# Create your views here.
from django.contrib.auth.models import User
from groups.models import FriendRequest


def requestFriend(request,recipient_id):
    user = request.user
    recipient = User.objects.get(pk= recipient_id)
    message = request.POST["message"]
    fr = FriendRequest(user=user,recipientUser=recipient,message=message)
    fr.save()


def approveFriendRequest(request,request_id):
    friendRequest = FriendRequest.objects.get(pk=request_id)
    friendRequest.status = 3
    
