from flask import Flask, jsonify, request
from database.urls import EnrichedUrl

# initialize our Flask application
app= Flask("api")


def search_function(query):
    #search function will search the EnrichedUrl table for the query and return the results
    #the database query will search the title, contents, keywords for the query
    #the results will be taken in different variables for title, contents, keywords

    title_results = EnrichedUrl.select().where(EnrichedUrl.title.contains(query))
    contents_results = EnrichedUrl.select().where(EnrichedUrl.contents.contains(query))
    keywords_results = EnrichedUrl.select().where(EnrichedUrl.keywords.contains(query))

    # create a set that will create a list of deduplicated results
    # first priority goes to title results, then keywords and then contents
    # this is done to ensure that the results are sorted in the order of priority
    # the results are then converted to a list and returned
    results_set = set(title_results) | set(keywords_results) | set(contents_results)
    results = list(results_set)
    return results

def jsonify_results(search_results):
    #this function creates a list of json objects from the search results
    #the json objects will contain the url, title, contents, keywords, url_hash, effective_url
    #the url is taken from the corresponding url entry in the UnenrichedUrl table through the foreign key

    json_results = []
    for result in search_results:
        json_object = {
            "url": result.url.link,
            "title": result.title,
            "keywords": result.keywords,
            "url_hash": result.url_hash,
            "effective_url": result.effective_url,
            "added_on": result.added_on
        }
        json_results.append(json_object)
    
    return json_results

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    search_query = args['q']

    raw_results = search_function(search_query)
    json_results = jsonify_results(raw_results)

    return jsonify(json_results)


app.run(debug=True, host="0.0.0.0", port=5000)