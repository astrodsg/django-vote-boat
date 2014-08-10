# Licensed under a 3-clause BSD style license - see LICENSE
# -*- coding: utf-8 -*-
"""
PURPOSE: Handles vote-boat models
DATE: Thu Jul 31 16:56:32 2014
"""
# ########################################################################### #
import datetime
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy 
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser

# ########################################################################### #

class User (models.Model):
    """ Create user accounts """
    # ----------------------- account type
    TMP_ACCOUNT = 0
    PERM_ACCOUNT = 1
    account_type = models.IntegerField(default=TMP_ACCOUNT)

    # ----------------------- User information
    username = models.CharField(max_length=30)
    first_name = models.CharField(ugettext_lazy('first name'), max_length=30, blank=True)
    last_name = models.CharField(ugettext_lazy('last name'), max_length=30, blank=True)
    email = models.EmailField(ugettext_lazy('email address'), max_length=254, blank=True,null=True)
    
    # ----------------------- information
    is_active = models.BooleanField(ugettext_lazy('active'), default=True,
        help_text=ugettext_lazy('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    creation_date = models.DateTimeField(ugettext_lazy('date joined'), default=timezone.now)
    last_login_date = models.DateTimeField(ugettext_lazy('last login'), default=timezone.now)    
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ["username","last_login_date"]

    def __unicode__(self):
        return u"User : {} {}".format(self.username,self.id)

    def get_absolute_url(self):
        return "/users/{}/".format(urlquote(self.email))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(self.first_name,self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        if self.email is not None:
            send_mail(subject, message, from_email, [self.email])

class Poll (models.Model):
    """ Create a set of ideas to vote on """
    # ----------------------- editable 
    title = models.CharField(max_length=100,help_text="Title")
    description = models.CharField(max_length=300,default="",help_text="Description",blank=True)
    admin_user_id = models.ForeignKey(User)    

    # ----------------------- added 
    admin_url = models.URLField(blank=True)
    participant_url = models.URLField(blank=True)    
    creation_date = models.DateTimeField(ugettext_lazy('created'), default=timezone.now)
    update_date = models.DateTimeField(ugettext_lazy('updated'), default=timezone.now)    
    
    def __unicode__ (self):
        return u"Poll : {}".format(self.title)

class IdeaTag (models.Model):
    """ Create tags for the ideas """
    tag = models.CharField(max_length=32)
    
    def __unicode__ (self):
        return self.tag
    
class Idea (models.Model):
    """ Create an idea to vote on """
    poll_id = models.ForeignKey(Poll,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300,default="",blank=True)
    users = models.ManyToManyField(User, through='Vote')
    tags = models.ManyToManyField(IdeaTag,blank=True)
    
    # ----------------------- times
    creation_date = models.DateTimeField(ugettext_lazy('created'), default=timezone.now)
    update_date = models.DateTimeField(ugettext_lazy('updated'), default=timezone.now)    
       
    def __unicode__ (self):
        return u"Idea : {}".format(self.title)   

class Vote (models.Model):
    """ Register a vote for a particular idea """
    # ----------------------- 
    idea_id = models.ForeignKey(Idea,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)    
    
    # ----------------------- times
    creation_date = models.DateTimeField(ugettext_lazy('created'), default=timezone.now)
    update_date = models.DateTimeField(ugettext_lazy('updated'), default=timezone.now)    
            
    # ----------------------- votes
    DOWN_VOTE = 0
    UP_VOTE = 1
    vote_value = models.IntegerField(null=True)
    
    comment = models.CharField(max_length=300,default="",blank=True)
    
    def __unicode__ (self):
        # TODO: get the username and the idea title        
        return "<Vote {} {}>".format(self.idea_id,self.user_id)
        
class PollVoteNumber (models.Model):
    # ----------------------- 
    poll_id = models.ForeignKey(Poll,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)    
    number_of_votes = models.IntegerField(default=0)

