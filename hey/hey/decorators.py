from django.http import HttpResponseRedirect

def myuser_login_required(f):
    def wrap(request, *args, **kwargs):
    #this check the session if userid key exist, if not it will redirect to login page
        for r in request.session.keys():
            print r
        if 'user_id' not in request.session.keys():
            return HttpResponseRedirect("/user/login")
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap