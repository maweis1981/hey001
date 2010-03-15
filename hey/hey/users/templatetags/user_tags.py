from django import template
from hey.users.models import User

register = template.Library()


def can_edit(userId):    
    s_user_id = str(request.session['user_id'])
    if userId == s_user_id:
        user = User.objects.get(pk=userId)
        return {'canEdit':True,'s_user':user}
    else:
        return {'canEdit':False}

register.simple_tag(can_edit)