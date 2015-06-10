Flask for ElasticSearch 
==================

I have built a nice search-engine template using Python Flask in the backend and providing faceted navigation in the frontend.

The frontend was built using:

http://materializecss.com/


Demo
----
![alt tag](https://raw.github.com/svola/ElasticUI-extension/master/doku/demo-materialize2.png)


Setup
----------

You need to edit 2 files accordingly to run your project.


1. fantasticsearch/views.py:

```
#TODO: Configuration
host = "http://localhost:9200"
indexName = "myIndex"
aggregationFields = ["field1", "field2"]
```

Basic queries with filters are already setup, but you can configure them according to your needs.
Currently it is implemented to support the most generic and powerful query_string_query:

http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax


2. fantasticsearch/templates/container.html

Inside the first row, please edit FIELD1 and FIELD2 according to your needs. 
And change the fieldnames inside the properties id and for to match your exact fieldnames as provided in the mapping.

```
    <input type="checkbox" id="field1-{{bucket.key}}">
    <label for="field1-{{bucket.key}}">{{bucket.key}} ({{bucket.doc_count}})</label>
```

Feel free to add more aggregations. 



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


