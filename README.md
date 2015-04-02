ElasticUI-extension
==================

ElasticUI is an awesome and very easy to setup framework that enables faceted navigation for ElasticSearch, written in AngularJS.

This is basically just an extension to the demo-template.


http://www.elasticui.com/

**Modifications:**

- Moved configurations into app.js
- Replaced MatchQuery with QueryStringQuery, as the syntax is more powerful

http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax

- Added formatting of result-set inspired by Calaca.
- Unifying results was also inspired by Calaca ("track by id")

https://github.com/romansanchez/Calaca

- Bootstrap is added, to support media-items for beautifully displaying images and standard attributes. 

http://getbootstrap.com/components/#media

- ng-elif is added to allow for easy case-control flow in the template. (add to module)
- In combination with the bootstrap media-objects, you can easily display different default-images based on features like category, etc. 

https://github.com/zachsnow/ng-elif

New features in the template

 - SignificantTerms aggregation
 - Sort using buttons (Could be enhanced)

TODO:
 
- Make it mobile-friendly


Documentation
---------------------

The main part of the project is borrowed from ElasticUI, so that's where a lot of documentation can be found.

https://github.com/YousefED/ElasticUI

I just wanted to make a template which has more features builtin in the template, so it could already be used as search-engine and needs just some design enhancements and configuration of queries to use in the backend. 


Setup
----------

Just edit js/app.js and enter your ElasticSearch-Host and index-name.
Then edit demo.html and change all your field-names accordingly.


Queries
----------

The queries that can be used easily in the backend are documented here:

https://github.com/fullscale/elastic.js/blob/master/dist/elastic.js
http://docs.fullscale.co/elasticjs/

And of course on the official ElasticSearch website.

http://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

One of the queries that can be used is MatchQuery with all it's parameters, that just need to be added like this in the template:


```
<input type="text" class="form-control" eui-query="ejs.MatchQuery('title', querystring).type('phrase')" ng-model="querystring" eui-enabled="querystring.length" />
```

All parameters can be added like this: 

ejs.QUERY_TYPE(REQUIRED_PARAMETERS).OPTIONAL_PARAMETERS(VALUE)


Mapping considerations
---------------------------------

Usually you don't need to create a mapping for an index with ElasticSearch, as it's schemaless, or better, creates a schema on the fly based on the first document.
BUT if you want to provide faceted navigation, you should create an explicit mapping. 
Per default each field is analyzed. 
A terms facet of an analyzed field, will show you the analyzed tokens.

Which looks like this:

![alt tag](https://raw.github.com/svola/ElasticUI-extension/master/doku/facet-bad.png)

What you want instead, is usually this:

![alt tag](https://raw.github.com/svola/ElasticUI-extension/master/doku/facet-good.png)

And for this you need to configure your mapping accordingly, before creating the index:

Usually you want the field both, intuitively searchable and "facetable", so you should use multifields like this:

```
"author" : {
      "type" : "string",
      "analyzer" : "english", #or standard, or any other language. For proper names, it's hard to find a "right way" 
      "fields": {
              "raw":   { "type": "string", "index": "not_analyzed" }
      }
}
```

Your **template** would then look like this:

```
<h3>Author</h3>
  <eui-checklist field="'author.raw'" size="10"></eui-checklist>
```
            
http://www.elastic.co/guide/en/elasticsearch/reference/current/_multi_fields.html


Security-considerations
--------------------------------

The app configured like this, is not secure at all. 
It works nice for development, but if you use the JS-client everybody can get access to your credentials.
Please consider this:

http://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/host-reference.html#_examples_2


Browser-compatibility
------------------------------

The app currently works with Chromium (41.xx on Ubuntu), but not with Firefox (36.xxon Ubuntu).


Demo
----

![alt tag](https://raw.github.com/svola/ElasticUI-extension/master/doku/demo.png)
