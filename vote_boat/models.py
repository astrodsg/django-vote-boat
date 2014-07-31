from django.db import models
import datetime
from django.utils import timezone

class Poll (models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300,default="")
    #    admin_user_id 

    def __unicode__ (self):
        return u"Poll : {}".format(self.title)

class Idea (models.Model):
    poll_id = models.ForeignKey(Poll)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300,default="")
    
    def __unicode__ (self):
        return u"Idea : {}".format(self.title)   