'''
wrapper.py
May 21st, 2019
By Daniel Kleber and Ginnie White

Code to handle the flask output using api.py
'''
import api
import sys
import flask
from flask import render_template, jsonify

app = flask.Flask(__name__)

flask_api = api.API()

@app.route('/')
def homePage():
    #refresh the API, just in case
    flask_api = api.API()
    return render_template('home.html')

@app.route('/readme')
def citationPage():
    return render_template('README.html')

@app.route('/search')
def advancedSearchPage():
    return render_template('advanced_search.html')

@app.route('/majors/all')
def allMajors():
    output_data = flask_api.getAllMajorsData()
    #lists all the majors by passing all of them to listMajors.html
    return render_template('listMajors.html', majorsList=output_data)

@app.route('/majors/rank')
def majorRankCall():
    major_rank = flask.request.args.get('major title')
    '''
    Method will attempt to use
    findMajorByRank to get the output data and render the page with the specific
    majordata, but if findMajorByRank throws an exception, then method returns
    an empty specific major page
    '''
    try:
        #get the data from the API
        output_data = flask_api.findMajorByRank(major_rank)
        totalJobSearchers = output_data["employed"] + output_data["unemployed"]
        #convert the dictionary that gives us into the dictionary we want
        output_data["major"] = output_data["major"].title()
        output_data["Rank"] = output_data["rank"]
        output_data["Major Category"] = output_data["major_category"]
        output_data["Portion Identifying as Female"] = output_data["sharewomen"]
        output_data["Unemployment Rate"] = output_data["unemployment_rate"]
        output_data["Portion with Full-Time Jobs"] =output_data["full_time"] / totalJobSearchers
        output_data["Portion with Part-Time Jobs"] = output_data["part_time"] / totalJobSearchers
        output_data["Portion with Full-Time Year-Round Jobs"] = output_data["full_time_year_round"] / totalJobSearchers
        output_data["Median Income"] = output_data["median"]
        output_data["25th Percentile Income"] = output_data["p25th"]
        output_data["75th Percentile Income"] = output_data["p75th"]
        output_data["Portion with Jobs Requiring a College Degree"] = output_data["college_jobs"] / totalJobSearchers
        output_data["Portion with Jobs Not Requiring a College Degree"] = output_data["non_college_jobs"] / totalJobSearchers
        output_data["Portion with Low-Wage Service Jobs"] = output_data["low_wage_jobs"] / totalJobSearchers
    except (TypeError, ValueError):
        #return an empty dict, and so a page with no data, if something went wrong
        output_data = {}
    #render the data into our HTML template
    return render_template('specific_major.html', specific_major = output_data,
    parametersList = ["Rank", "Major Category", "Portion Identifying as Female",
    "Portion with Full-Time Jobs", "Portion with Part-Time Jobs", "Portion with Full-Time Year-Round Jobs",
    "Unemployment Rate", "Median Income", "25th Percentile Income", "75th Percentile Income",
    "Portion with Jobs Requiring a College Degree", "Portion with Jobs Not Requiring a College Degree",
    "Portion with Low-Wage Service Jobs"])

@app.route('/majors/name')
def majorNameCall():
    major_name = flask.request.args.get('major_title')
    '''
    Method will attempt to use findMajorByName to get the output data and render
    the page with the specific major data, but if findMajorByRank throws an
    exception, then method returns an empty specific major page
    '''
    try:
        #get the data from the API
        output_data = flask_api.findMajorByName(major_name.upper())
        totalJobSearchers = output_data["employed"] + output_data["unemployed"]
        #convert the dictionary that gives us into the dictionary we want
        output_data["major"] = output_data["major"].title()
        output_data["Rank"] = output_data["rank"]
        output_data["Major Category"] = output_data["major_category"]
        output_data["Portion Identifying as Female"] = output_data["sharewomen"]
        output_data["Unemployment Rate"] = output_data["unemployment_rate"]
        output_data["Portion with Full-Time Jobs"] =output_data["full_time"] / totalJobSearchers
        output_data["Portion with Part-Time Jobs"] = output_data["part_time"] / totalJobSearchers
        output_data["Portion with Full-Time Year-Round Jobs"] = output_data["full_time_year_round"] / totalJobSearchers
        output_data["Median Income"] = output_data["median"]
        output_data["25th Percentile Income"] = output_data["p25th"]
        output_data["75th Percentile Income"] = output_data["p75th"]
        output_data["Portion with Jobs Requiring a College Degree"] = output_data["college_jobs"] / totalJobSearchers
        output_data["Portion with Jobs Not Requiring a College Degree"] = output_data["non_college_jobs"] / totalJobSearchers
        output_data["Portion with Low-Wage Service Jobs"] = output_data["low_wage_jobs"] / totalJobSearchers
    except ValueError:
        #return an empty dict, and so a page with no data, if something went wrong
        output_data = {}
    #render the data into our HTML template
    return render_template('specific_major.html', specific_major = output_data,
    parametersList = ["Rank", "Major Category", "Portion Identifying as Female",
    "Portion with Full-Time Jobs", "Portion with Part-Time Jobs", "Portion with Full-Time Year-Round Jobs",
    "Unemployment Rate", "Median Income", "25th Percentile Income", "75th Percentile Income",
    "Portion with Jobs Requiring a College Degree", "Portion with Jobs Not Requiring a College Degree",
    "Portion with Low-Wage Service Jobs"])


@app.route('/results')
def searchRunner():
    '''
    Method will attempt to use filterAndSortMajors to get the output data and
    render the page with the info for all majors that fit the parameters sorted
    in the requested directions, but if filterAndSortMajors throws an exception,
    then method returns an empty search majors page
    '''
    filters_list = []
    sorts_list = []

    major_category = flask.request.args.get('Category')
    if(major_category not in ("", " ")):
        filters_list.append(('major_category', '=', major_category))
    for offset in range(1,7):
        filters_list = checkAppendFilter(flask.request.args, offset, filters_list)
    for offset in range(1,3):
        sorts_list = checkAppendSort(flask.request.args, offset, sorts_list)
    #use gets to populate the above two lists
    try:
        output_data = flask_api.filterAndSortMajors(filters_list, sorts_list)
        #actually run the request by calling the API
    except ValueError as e:
        #if something was invalid, output a page with no data
        output_data = []
        #Bug catching code so we know what went wrong if something goes wrong
        print("I'm throwing an exception! " + str(e))
    #Render the data into our listMajors template and output it
    return render_template('listMajors.html', majorsList=output_data)

def checkAppendFilter(flask_dict, offset, filters_list):
    #Check if the filter at number "offset" is filled in. If so, add it to the
    #list as a tuple. Helper method for searchRunner.
    if(flask_dict.get('Criterion' + str(offset)) not in  ("", " ", None)
       and flask_dict.get('Comparison' + str(offset)) not in  ("", " ", None)
       and flask_dict.get('Value' + str(offset)) not in  ("", " ", None)):
        filters_list.append((flask_dict.get('Criterion' + str(offset)),
                             flask_dict.get('Comparison' + str(offset)),
                             flask_dict.get('Value' + str(offset))))
    return filters_list

def checkAppendSort(flask_dict, offset, sorts_list):
    #Check if the sort at number "offset" is filled in. If so, add it to the
    #list as a tuple. Helper method for searchRunner.
    if(flask_dict.get('SortBy' + str(offset))) not in ("", " ", None):
        if (flask_dict.get('Order' + str(offset))) not in ("", " ", None):
            order = flask_dict.get('Order' + str(offset))
        else:
            order = ""
        sorts_list.append((flask_dict.get('SortBy' + str(offset)), order))
    return sorts_list

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
        exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
