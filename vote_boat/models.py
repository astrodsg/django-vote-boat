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
    """ Create user accounts
    """
    # ----------------------- account type
    TMP_ACCOUNT = 0
    PERM_ACCOUNT = 1
    account_type = models.IntegerField(default=TMP_ACCOUNT)

    # ----------------------- User information
    username = models.CharField(max_length=30,unique=True)
    first_name = models.CharField(ugettext_lazy('first name'), max_length=30, blank=True)
    last_name = models.CharField(ugettext_lazy('last name'), max_length=30, blank=True)
    email = models.EmailField(ugettext_lazy('email address'), max_length=254, blank=True,null=True)
    
    # ----------------------- information
    is_active = models.BooleanField(ugettext_lazy('active'), default=True,
        help_text=ugettext_lazy('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(ugettext_lazy('date joined'), default=timezone.now)
    last_login = models.DateTimeField(ugettext_lazy('date joined'), default=timezone.now)    
    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return u"User : {}".format(self.username)

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

    # ----------------------- editable 
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300,default="",blank=True)
    admin_user_id = models.ForeignKey(User)    

    # ----------------------- added 
    admin_url = models.URLField(blank=True)
    participant_url = models.URLField(blank=True)    
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)    
    def __unicode__ (self):
        return u"Poll : {}".format(self.title)

class Idea (models.Model):
    poll_id = models.ForeignKey(Poll,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300,default="")
    
    def __unicode__ (self):
        return u"Idea : {}".format(self.title)   

    

    
    