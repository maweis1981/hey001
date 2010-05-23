from django.contrib import admin
from votes.models import Poll, Choice, Vote

class PollAdmin(admin.ModelAdmin):
    pass

class ChoiceAdmin(admin.ModelAdmin):
    pass
    
class VoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Poll,PollAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(Vote,VoteAdmin)


