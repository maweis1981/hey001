import os
from decimal import Decimal
from datetime import datetime

from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpResponse,HttpResponseServerError,HttpResponseServerError
from django.utils import simplejson as json
from django.utils.encoding import force_unicode
from django.utils.functional import Promise


def expect_post_request(func):
    """Allow only POST requests to come in, throw an exception otherwise.

    This relieves from checking every time that the request is
    really a POST request, which it should be when using this
    decorator.
    """
    def _ret(*args, **kwargs):
        ret = func(*args, **kwargs)
        request = args[0]
        if not request.method=='POST':
            raise Exception('POST request expected.')
        return ret
    return _ret

def add_request_getdict(func):
    """Add the method getdict() to the request object.

    This works just like getlist() only that it decodes any nested
    JSON encoded object structure.
    Since sending deep nested structures is not possible via
    GET/POST by default, this enables it. Of course you need to
    make sure that on the JavaScript side you are also sending
    the data properly, which dojango.send() automatically does.
    Example:
        this is being sent:
            one:1
            two:{"three":3, "four":4}
        using
            request.POST.getdict('two')
        returns a dict containing the values sent by the JavaScript.
    """
    def _ret(*args, **kwargs):
        args[0].POST.__class__.getdict = __getdict
        ret = func(*args, **kwargs)
        return ret
    return _ret

def __getdict(self, key):
    ret = self.get(key)
    try:
        ret = json.loads(ret)
    except ValueError: # The value was not JSON encoded :-)
        raise Exception('"%s" was not JSON encoded as expected (%s).' % (key, str(ret)))
    return ret

def json_response(func):
    """
    """
    def _ret(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret==False:
            ret = {'success':False}
        elif ret==None: # Sometimes there is no return.
            ret = {}
        # Add the 'ret'=True, since it was obviously no set yet and we got valid data, no exception.
        if not ret.has_key('success'):
            ret['success'] = True
        json_ret = ""
        try:
            # Sometimes the serialization fails, i.e. when there are too deeply nested objects or even classes inside
            json_ret = json_resp(ret)
        except Exception, e:
            print '\n\n===============Exception=============\n\n'+str(e)+'\n\n'
            print ret
            print '\n\n'
            return HttpResponseServerError(content=str(e))
        return json_ret
    return _ret


def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to an object dynamically are being ignored (and it also has
    problems with some models).
    """

    def _any(data):
        ret = None
        # Opps, we used to check if it is of type list, but that fails
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data)
        # Same as for lists above.
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, Model):
            ret = _model(data)
        # here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
        elif isinstance(data, basestring):
            ret = unicode(data)
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_unicode(data)
        elif isinstance(data, datetime):
            # For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
            # i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
            ret = str(data).replace(' ', 'T')
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

def json_resp(data):
    data = json_encode(data)
    print data
    mimetype = "text/json"
    ret = HttpResponse(data, mimetype=mimetype+"; charset=UTF-8")
    # The following are for IE especially
    ret['Pragma'] = "no-cache"
    ret['Cache-Control'] = "must-revalidate"
    ret['If-Modified-Since'] = str(datetime.now())
    return ret
