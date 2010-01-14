# -*- coding: UTF-8 -*-
# e-Linguistics Toolkit: jsonutils 
#
# Copyright (C) 2009 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT
"""
The jsonutils module contains tools to create JSON data from various ELTK objects.
"""


from eltk.kb.Meta import *
import json


from eltk.reader.LinkedDataReader import *
from eltk.config import ELTK_HOME
    


reader = LinkedDataReader()
  
GOLD_graph = reader.parseGraph('/home/farrar/svn_projects/goldcomm/gold/gold-2009.owl')
GOLD = reader.buildPyModel()
 


"""
The ComplexEncoder class is an extension that creates JSON compatible with the javascript Extjs.TreePanel class.
"""
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        
        #if the obj is a class
        if isinstance(obj,OWLClass):
            
            #children, as in child nodes in a tree structure
            children = []

            #if the class has subclasses
            if obj.getSubClasses() is not None: 
                
                #
                for c in obj.getSubClasses():
                    
                    #recursive step
                    children.append(self.default(c))
               
            #iterate over instances, if any
            for i in obj.getInstances():
                #create the code for the JSON dump
                children.append(self.makeInstance(i))
                
            
            return {'text':obj.name, 'cls':'folder', 'uri':obj.uri,'children':children}
        
        
        #if the obj is an instance
        elif isinstance(type(obj),OWLClass):
            return self.makeInstance(obj) 
        
        #returns the json encoded data
        return json.JSONEncoder.default(self, obj)
   
    
    def makeInstance(self,inst):
        """
        Necessary so that JSON doens't turn everything into a string during a recursive dump.
        :param inst: an instance of an OWLClass
        :type inst: OWLClass
        :rtype: dict
        """
        return {'text':inst.name, 'uri':inst.uri,'leaf':True} 

    #def makeClass(self,cls):
    #    children
    #    if cls.getInstances != []:
    #

    #    return {'text':cls.name, 'cls':'folder', 'uri':cls.uri,'children':[]}








if __name__=='__main__':
    #Word = OWLClass.new('http://foo.org/Word')
    #print type(Word)
    #w1 = Word(u'http://foo.org/word123')
    
    

   
    #outfile = open(ELTK_HOME+'/examples/outputfiles/concepts.json','w')
    #outfile = open('/home/farrar/svn_projects/lingdesktop/htdocs/media/json/features.json','w')
    #outfile = open('/home/farrar/svn_projects/lingdesktop/htdocs/media/json/POS.json','w')
    #outfile = open('/home/farrar/svn_projects/lingdesktop/htdocs/media/json/PhoneticProperty.json','w')
    #outfile = open('/home/farrar/svn_projects/lingdesktop/htdocs/media/json/LinguisticUnit.json','w')
    outfile = open('/home/farrar/svn_projects/lingdesktop/htdocs/media/json/MorphosemanticProperty.json','w')

    
    #test cls w no subclasses
    #outfile.write('['+json.dumps(GOLD.TenseProperty, cls=ComplexEncoder, indent=4)+']')
    
    #test class w only an instance
    #outfile.write('['+json.dumps(GOLD.PastTense, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
    
    #test class w subclasses
    #outfile.write('['+json.dumps(GOLD.LinguisticProperty, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
    #outfile.write('['+json.dumps(GOLD.PartOfSpeechProperty, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
    #outfile.write('['+json.dumps(GOLD.PhoneticProperty, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
    #outfile.write('['+json.dumps(GOLD.LinguisticUnit, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
    outfile.write('['+json.dumps(GOLD.MorphosemanticProperty, cls=ComplexEncoder, sort_keys=True, indent=4)+']')
