from django import template
from hey.users.models import User
from hey.users.tags import can_edit

register = template.Library()


def can_edit(context,userId):
    request = context['request']
    s_user_id = str(request.session['user_id'])
    if userId == s_user_id:
        user = User.objects.get(pk=userId)
        return {'canEdit':True,'s_user':user}
    else:
        return {'canEdit':False}

register.simple_tag(can_edit)