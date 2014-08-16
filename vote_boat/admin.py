from django.contrib import admin

from django.contrib import admin
from vote_boat.models import Poll,IdeaTag,Idea,User,Vote

class UserAdmin (admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','email')

class PollAdmin (admin.ModelAdmin):
    list_display = ('id','title','creation_date','admin_url','participant_url')
    
class VoteAdmin (admin.ModelAdmin):
    list_display = ('user_id','idea_id','vote_value')
    search_fields = ['user_id',"idea_id"]
        
class IdeaAdmin (admin.ModelAdmin):
    list_display = ("poll_id","title","creation_date")
    admin_order_field = "poll_id"
    list_filter = ('poll_id',)


admin.site.register(Poll,PollAdmin)
admin.site.register(IdeaTag)
admin.site.register(Idea,IdeaAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Vote,VoteAdmin)

