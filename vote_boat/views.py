import re 

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.request import QueryDict

from vote_boat.models import Poll,User,Idea
from vote_boat.forms import PollForm,UsernameForm


def ideas (request,poll_ideas_url):
    """ Primary ideas page
    
    """
    # get request context
    context = RequestContext(request)

    s = re.search("(.*)-(\d*)$",poll_ideas_url.replace("_"," "))    
    poll_name = s.groups()[0]
    poll_id = s.groups()[1]

    try:    
        poll = Poll.objects.get(id=poll_id)
        # poll = Poll.objects.filter(admin_url=poll_ideas_url)
    except Poll.DoesNotExist as e: 
        # TODO: something better
        raise e
    
    # get all ideas
    # TODO: check context for something which says how to sort the ideas
    # TODO: think: optimize? should we figure out and sort different sortings?
    ideas = Idea.ideas_by_poll(poll)    
    
    # create context objects
    context_dict = dict(ideas=ideas,poll=poll)
    
    return render_to_response(template,context_dict,context)
    
def create_new_poll (template,successful_response):
    def new_poll (request):
        # get request context
        context = RequestContext(request)
    
        if request.method == 'POST':
            username = request.POST['username']
            # create new user                    
            user = UsernameForm(request.POST)
            if user.is_valid():
                user.save(commit=True)
                # TODO: better way to find the saved user
                admin = User.objects.latest('creation_date')            
            else:
                print(user.errors)            
                raise ValueError("figure out what to do here")
            post = request.POST
            kws = {k:request.POST[k] for k in ('title','description')}
            kws['admin_user_id'] = admin
            poll = PollForm(request.POST,instance=Poll(**kws))
            
            if poll.is_valid():
                poll.save(commit=True)                
                # next location
                return successful_response(request)
            else:
                print(poll.errors)                
        else:
            user = UsernameForm()     
            poll = PollForm()   
        context_dict = {'poll': poll,'user':user}
        return render_to_response(template, context_dict, context)
    return new_poll


# Poll page : set title, description, username, email, set admin_url, paricipant_url
# Add ideas page : add ideas
# settings : poll parameters (e.g. freeze date)
# Finish : email admin, show admin_url, participant_url : Invite participants

# admin_poll_page :







