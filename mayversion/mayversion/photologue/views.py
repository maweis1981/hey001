from django.template import  Context,loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from photologue.models import Gallery ,Photo
from django.conf import settings


# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)
# galleries
gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}

@login_required
def gallery_index(request):
    user = request.user
#    latest = Photo.objects.filter(user=user)
    latest = Gallery.objects.filter(is_public=True)
    sample_size = SAMPLE_SIZE
    return render_to_response('photologue/photo_archive.html', locals())

