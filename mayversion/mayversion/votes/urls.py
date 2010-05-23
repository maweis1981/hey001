from django.conf.urls.defaults import *
from votes.forms import ChoiceForm

urlpatterns = patterns('votes.views',
    url(r'^vote/(?P<vote_id>\d+)/$', 'vote', name='single_vote'),
    url(r'^votes$', 'listVotes', name='votes'),
    url(r'^newPoll/$', 'newPoll',
          {'form_class': ChoiceForm, 'template': 'votes/inline-formset.html'}, name='example_inline_formset'),
          
)
