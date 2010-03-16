# Create your views here.
from django.contrib.auth.decorators import login_required
import django.shortcuts
from django.contrib.auth.models import User

from django.shortcuts import render_to_response,get_object_or_404
from datings.models import Dating

@login_required
def detail(request,dating_id):
    user = request.user
    dating = get_object_or_404(Dating,pk = dating_id)

    return render_to_response('dating/detail.html',locals())
