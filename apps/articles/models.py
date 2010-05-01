import urllib2
from xml.dom import minidom
from datetime import datetime, timedelta

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django import forms 

class HNItems(models.Model):
    """ List of HN Items """
    itemid = models.CharField('HN Item Id', max_length=20)
    link = models.CharField('Link', max_length=250)
    header = models.TextField('Link Header', null=True, blank=True)    
    score = models.IntegerField('Score', null=True, blank=True)
    user_id = models.CharField('Code', max_length=200, null=True, blank=True)
    user_name = models.CharField('Name', max_length=200, null=True, blank=True)
    comments = models.IntegerField('Comments', null=True, blank=True)
    linkcontents = models.TextField('Link Contents', null=True, blank=True)
    linkcomments = models.TextField('Link Comments', null=True, blank=True)
    linktype = models.SmallIntegerField('Link OR Comments', default=1)
    
    def __unicode__(self):
        return self.itemid
