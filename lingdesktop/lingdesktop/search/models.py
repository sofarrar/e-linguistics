# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt


from django.db import models


class URIField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        #kwargs['max_length'] = 104
        kwargs['verify_exists'] = False
        
        super(URIField, self).__init__(*args, **kwargs)
        

    def dereference(self):
        """
        possibly useful, decide later
        """
        pass

class URIModel(models.Model):
    uri = URIField(primary_key = True)
    #uri = URIField()
    
    label =  models.CharField(max_length=30)
    comment = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.uri

class WordModel(models.Model):
    word =  models.CharField(max_length=50,primary_key = True)
    uri = models.ManyToManyField(URIModel)
    #uri = models.ForeignKey(URIModel) 
    
    #URIField()

    def __unicode__(self):
        return self.word

    #class Meta:
    #    ordering = ('word')
