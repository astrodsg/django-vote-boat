from django import forms
from vote_boat.models import Poll, User


class PollForm (forms.ModelForm):    
    description = forms.CharField(max_length=300,required=False)
    # create a new user
    # username = forms.CharField(max_length=30)
    admin_user_id = forms.IntegerField
       
    class Meta:
        model = Poll
        exclude = ('admin_user_id','admin_url','participant_url','creation_date', 'update_date')
        
    def __init__ (self, *args, **kwargs):
        # style the new poll form
        forms.ModelForm.__init__(self, *args, **kwargs)
        for key in ["title","username","email"]:
            self.feilds[key].widget.attrs.update({'class' : 'vote_boat_input' })
        
        # set up the description formatting
        self.fields["description"].widget = forms.Textarea
        self.fields["description"].widget.attrs.upddate('class': 'vote_boat_text_area')
            
    
        
class UsernameForm (forms.ModelForm):
    username = forms.CharField(max_length=30,help_text="Username:")
    email = forms.EmailField(max_length=254,required=False,help_text="email:")
    
    class Meta:
        model = User
        exclude = ('account_type','first_name','last_name','is_active','creation_date','last_login_date')
        

