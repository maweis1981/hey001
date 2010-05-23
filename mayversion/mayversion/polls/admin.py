from polls.models import Poll,Choice,Vote
from django.contrib import admin

class PollAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('title', 'user')
    ordering = ['pub_date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
            (None, {
                'fields': ('title', 'description', 'user', 'ip_address')
            }),
            (('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('state', 'slug',)
            }),
        )
 
    
class ChoiceAdmin(admin.ModelAdmin):
    pass
    
class VoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('poll', 'choice', 'user')
    ordering = ['pub_date']
    search_fields = ['poll']
    fieldsets = (
              (None, {
                  'fields': ('poll', 'choice', 'user', 'ip_address')
              }),
              (('Advanced settings'), {
                  'classes': 'collapse',
                  'fields' : ()
              }),
          )



admin.site.register(Poll,PollAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(Vote,VoteAdmin)


