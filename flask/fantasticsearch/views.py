import flask
from flask import render_template
from flask import request
from flask import make_response
from fantasticsearch import fantasticsearch
from elasticsearch import Elasticsearch

#TODO: Move to config
es = Elasticsearch()
indexName = "english"

@fantasticsearch.route('/')
def index():
	term = "MATCH_ALL"

	results = performQuery(term, "", 0)
	
	return render_template('index.html', results=results, term=term, page=1)


@fantasticsearch.route('/search')
def search():
	term = request.args.get('term', '')
	filters = request.args.get('filter', '')
	page = request.args.get('page', '')

	if not term:
		term = "MATCH_ALL"

	results = performQuery(term, filters, page)
	
	if page:
		page = int(page) + 1	

	return render_template('index.html', results=results, filters=filters, term=term, page=page)



def performQuery(term, filterString, page):

	filters = parseFilters(filterString)

	term = term.encode('utf-8')			
	query = getQuery(filters, term, page)	

	print query

	result = es.search(index=indexName, body=query)

	return result 


def parseFilters(filters):
	filterDict = {}
	for f in filters.split(','):
		if f and len(f.split('-')) == 2: 	
			typ = f.split('-')[0].encode('utf-8')
			val = f.split('-')[1].encode('utf-8')
			filterDict[typ] = val
	
	return filterDict


def getQuery(filters, term, page):
	query = None
	
	if not page:
		page = 0
	start = int(page) * 12

	if (term == "MATCH_ALL" or term == "null") and filters:
		mustClauses = []
		for k,v in filters.iteritems():
			clause = {"term" : { k : v }}
                	mustClauses.append(clause)	
		filters = {"and" : mustClauses }	

		
		query = {
		   "query": {
		      "function_score": {
			 "query": {
			    "filtered": {
			       "filter": filters,
			       "query": { 
					"match_all": {}
				}
			       }
			   },
			  "functions": [
			    {
			       "script_score": {
				  "script": "_score * (100 - doc['unknownVoc'].value)"
			       }
			    }
			 ]
		      }
		   },
		   "size": 12,
		   "from": start,
		   "aggs": {
		      "level": {
			 "terms": {
			    "field": "level"
			 }
		      },
		      "mediaType": {
			 "terms": {
			    "field": "mediaType"
			 }
		      }
		   },
		   "_source": [
		      "title",
		      "author",
		      "link",
		      "level",
		      "lix",
		      "unknownVoc",
		      "imageUrl"
		   ]
		}

	elif (term == "MATCH_ALL" or term == "null"):
		query = {
		   "query": {
		      "function_score": {
			 "query": {
				"match_all": {}
			  },
			  "functions": [
			    {
			       "script_score": {
				  "script": "_score * (100 - doc['unknownVoc'].value)"
			       }
			    }
			 ]
		      }
		   },
		   "size": 12,
		   "from": start,
		   "aggs": {
		      "level": {
			 "terms": {
			    "field": "level"
			 }
		      },
		      "mediaType": {
			 "terms": {
			    "field": "mediaType"
			 }
		      }
		   },
		   "_source": [
		      "title",
		      "author",
		      "link",
		      "level",
		      "lix",
		      "unknownVoc",
		      "imageUrl"
		   ]
		}


	elif term and filters:
		mustClauses = []
		for k,v in filters.iteritems():
			clause = {"term" : { k : v }}
                	mustClauses.append(clause)	
		filters = {"and" : mustClauses }	

		print filters	

		query = {
			   "query": {
			      "function_score": {
				 "query": {
				    "filtered": {
				       "filter": filters,
				       "query": {
					  "multi_match": {
					     "query": term,
					     "fields": [
						"title^3",
						"keywords^2",
						"category^2",
						"text",
						"author"
					     ]
					  }
				       }
				    }
				 },
				 "functions": [
				    {
				       "script_score": {
					  "script": "_score * (100 - doc['unknownVoc'].value)"
				       }
				    }
				 ]
			      }
			   },
			    "aggs" : {
				"level" : {
				    "terms" : { "field" : "level" }
				},
				"mediaType" : {
				    "terms" : { "field" : "mediaType" }
				}
			    },
			    "_source" : ["title", "author", "link", "level", "lix", "unknownVoc", "imageUrl"],
			   "size": 12,
			   "from": start
			}
		

	elif term:
		query = { "query": {
   				 "function_score": {
    					  "query": 
						{  "multi_match" : { 
							"query" : term,
							 "fields" : ["title^3", "keywords^2", "category^2","text", "author"]
		   					}
      					},
      					"functions": [
        					{"script_score": {
           						 "script": "_score * (100 - doc['unknownVoc'].value)"
          							}
        							}
      							]
    						}
  				},
				    "aggs" : {
					"mediaType" : {
					    "terms" : { "field" : "mediaType" }
					},
					"level" : {
					    "terms" : { "field" : "level" }
					}
				    },
			    	"_source" : ["title", "author", "link", "level", "lix", "unknownVoc", "imageUrl"],
  				"size" : 12,
				"from" : start
			}
		

	return query
		 		
