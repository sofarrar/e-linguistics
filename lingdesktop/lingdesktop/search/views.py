# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt


from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.utils import simplejson

from lingdesktop.search.models import WordModel
from lingdesktop.search.models import URIModel


from rdflib import plugin, exceptions
from rdflib.store import Store
from rdflib.Graph import ConjunctiveGraph

from eltk.config import ELTK_HOME
from eltk.config import STORE_CONFIG 
from eltk.namespace import *
from eltk.utils.sparql import *    



def serveforum(request):
    
    return render_to_response('search/topics-remote.json',{})



def servejson(request):
    
    return render_to_response('search/concepts.json',{})

def forumsearch(request):

    return render_to_response('search/forumsearch.html',{})



def searchpage(request):

    return render_to_response('search/searchpage.html',{})


def textSearch(request):
    return HttpResponse(simplejson.dumps({'success': True}))


def results(request):
    
    #request.POST values are always strings
    subj_uri = request.POST['subject']
    pred_uri = request.POST['predicate']
    obj_uri = request.POST['object']
   
    #begin SQARQL query

    return render_to_response('search/results.html', {'result': [subj_uri,pred_uri,obj_uri]})


    


def findword(request):
    """
    Used in 'quicksearch', this function retrieves a concept's label and comment.
    """

    test = '{"success":true, "resultset":[{"label":"a label","comment":"a comment"}]}'
    print test
    return HttpResponse(test)

    query = request.POST['query']
    
    error_result = '{"success":false}'
    
    #print query, '***************' 
    
    json_result=''
    
    try:
        query_set = WordModel.objects.filter(word__istartswith=query) 
       
        if len(query_set)==0: 
            return HttpResponse(error_result)
    
        #custom json hack to massage into extjs's format
        json_result = '{"success":true,"resultset":['
        
        
        for word_model in query_set:
            
        
            for u in word_model.uri.all():
                json_result = json_result+ '{"label":"'+u.label+'",'
                json_result = json_result+ '"comment":"'+u.comment+'"},'
        json_result = json_result+']}'

        
        print json_result
        
        return HttpResponse(json_result)

    except:
        #error_result = '{"resultset":[{"label":"No results for \''+query+'\'","comment":""}]}'
        return HttpResponse(error_result)

    

def sparqlquery(request):
    query = request.POST['query'] 
    #query = request.POST['query-textarea']
    #print query  

    
    store = plugin.get('MySQL', Store)() #('GOLDComms_id')
    
    #convert to config string compatible w RDFLIB
    rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']
    
    #open
    store.open(rdflib_config_string, create=False)
    graph1=''
    graph2=''


    cg = ConjunctiveGraph(store)
    
    #results = sparqlQuery('SELECT ?o WHERE {?s rdfs:comment ?o } ',graph1)
    #results = sparqlQuery("SELECT ?s WHERE {?s gold:orthographicRep 'karhulle' } ",graph2)




    results = sparqlQuery(u'SELECT  ?o WHERE {<http://purl.org/linguistics/gold#%s> rdfs:comment ?o }' % query ,cg)

    #print results

    if results is None:
        return
    else:
        return HttpResponse(simplejson.dumps({'success': True, 'totalCount':'1','results': [{'label':query, 'comment':results[0][0]}]}))

    #return HttpResponse(simplejson.dumps({'success': True}))
    #return HttpResponse(simplejson.dumps({'success': False}))
    #print 'error'
    """ 
    try:

        return HttpResponse(simplejson.dumps({'success': True, 'totalCount':'2','results': [{'label':'ProperNoun', 'comment':'and here\'s a comment about ProperNouns'},{'label':'Noun', 'comment':'and here\'s a comment about Nouns'},{'label':'ProperNoun', 'comment':'and here\'s a comment about ProperNouns'},{'label':'Noun', 'comment':'and here\'s a comment about Nouns'},{'label':'ProperNoun', 'comment':'and here\'s a comment about ProperNouns'},{'label':'Noun', 'comment':'and here\'s a comment about Nouns'},{'label':'ProperNoun', 'comment':'and here\'s a comment about ProperNouns'},{'label':'Noun', 'comment':'and here\'s a comment about Nouns'}]}))

    except:
        return HttpResponse(simplejson.dumps({'success': False}))
    
    """


#put this in a forms module ???
from django import forms

class ContactForm(forms.Form):
    class Media:
        css = {
            'all': ('css/input.css','css/background.css')
        }


    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)



def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('search/contact.html', {
        'form': form,
    })



