#!/usr/bin/env python
# encoding: utf-8

import os.path
from django.conf import settings
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from hey.avatar_crop.forms import AvatarForm, AvatarCropForm
from hey.avatar.models import Avatar
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from hey.avatar_crop import AVATAR_CROP_MAX_SIZE
from hey.avatar import AVATAR_STORAGE_DIR

from hey.users.models import User
from django.core.context_processors import csrf

#@login_required
def avatar_crop(request, id=None):
    """
    Avatar management, creates a new avatar and makes it default
    """

    user = User.objects.get(pk=1)

    if id:
        user = User.objects.get( pk = id)
        avatar = get_object_or_404(Avatar, id=id, user=user)
        print avatar
    else:
        avatar = get_object_or_404(Avatar, user=user, primary=True)
    if (avatar.avatar.width<=avatar.avatar.height):
        result = "width"
    else:
        result = "height"
    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        try:
            orig = avatar.avatar.storage.open(avatar.avatar.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return
        form = AvatarCropForm(image, request.POST)
        if form.is_valid():
            top = int(form.cleaned_data.get('top'))
            left = int(form.cleaned_data.get('left'))
            right = int(form.cleaned_data.get('right'))
            bottom = int(form.cleaned_data.get('bottom'))

            box = [ left, top, right, bottom ]
            (w, h) = image.size
            if result=="width":
                box = map(lambda x: x*h/AVATAR_CROP_MAX_SIZE, box)
            else:
                box = map(lambda x: x*w/AVATAR_CROP_MAX_SIZE, box)
            image = image.crop(box)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            thumb = StringIO()
            image.save(thumb, "JPEG")
            thumb_file = ContentFile(thumb.getvalue())
            base_name, ext = os.path.splitext(avatar.avatar.name)
            thumb = avatar.avatar.storage.save("%s_cropped%s" % (base_name, ext), thumb_file)
            Avatar.objects.filter(id=avatar.id).update(primary=False)
            new_avatar = Avatar(user=user, primary=True, avatar=thumb)
            new_avatar.save()
            user.message_set.create(message="修改了头像")
            
            return HttpResponseRedirect(reverse("avatar_change",args=(user.id,)))

    c = {
    'AVATAR_CROP_MAX_SIZE':AVATAR_CROP_MAX_SIZE,
    'dim':result,
    'avatar': avatar,
    'form': form
    }
    c.update(csrf(request))
    return render_to_response("avatar_crop/crop.html", c)

