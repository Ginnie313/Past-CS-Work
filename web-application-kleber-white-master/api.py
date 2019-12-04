'''
api.py
May 16th, 2019
By Daniel Kleber and Ginnie White

Code to set up and use an API with information about college majors in conjunction
with Flask and a database hosted on Perlman.

Note: This code deals purely with the API side of things and does not interact
with Flask from here (that's handled in wrapper.py)

'''
import flask
from flask import render_template, jsonify
import config
import psycopg2
import psycopg2.sql as sql
import psycopg2.extras
from decimal import *
import sys


class API:
    cursor = None
    connection = None

    def __init__(self):
        """
        Method finds the information from the database provided in config
        """
        from config import database
        from config import user
        # Connect to the database
        try:
            self.connection = psycopg2.connect(database=database, user=user, cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception as e:
            print(e)


        self.cursor = self.connection.cursor()


    def findMajorByRank(self, major_rank):
        '''
        Return a dictionary with all of the information about the major with a given rank.
        Throws a value error if the rank isn't valid (0 or less, or greater than 173) or
        a Type Error if the input can't be converted into a string.

        ex) findMajorByRank(1) should return:
        {"rank": 1, "major_code": 2419, "major": "PETROLEUM ENGINEERING",
        "total": 2339, "men": 2057, "women:": 282, "major_category": "Engineering",
        "sharewomen": 0.120564344, "sample_size": 36, "employed": 1976,
        "full_time": 1849, "part_time":270, "full_time_year_round": 1207, "unemployed": 37,
        "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000. "p75th":125000,
        "college_jobs": 1534, "non_college_jobs":364, "low_wage_jobs":193}

        '''
        SpecificMajor = {}
        #Error handling
        try:
            if int(major_rank) <= 0 or int(major_rank) > 173:
                raise Exception("Usage: The value of major_rank is too high or too low")
            query = 'SELECT * FROM majorsInformation WHERE rank = %s'
            self.cursor.execute(query, (str(major_rank),))
        except ValueError as err:
            raise TypeError("You must input something which can be converted to an integer!") from err
        except Exception as e:
            print(Exception)
            raise ValueError(e) from e

        #Gets all information about the specific major
        for row in self.cursor:
            SpecificMajor = row
        return SpecificMajor

    def filterMajorsBy(self, input_criterion, comparison, compare_value):
        '''
        Returns a byte string that can be used in an SQL query to get information from
        the database on majors fitting the relevant criterion with the right comparison
        to the compare value. Raises a ValueError if either the input_criterion or
        the comparison aren't valid

        ex) filterMajorsBy("unemployment_rate", "greater_than", "0.05")
            returns b"unemployment_rate > '0.05'"
        '''

        queryString = ""
        queryList = ["rank", "major_category", "shareWomen", "unemployment_rate",
        "median", "p25th", "p75th"]

        #Error handling
        if input_criterion not in queryList:
            raise ValueError("Usage: input_criterion must be a valid property of a major")
        if comparison not in ["greater_than", "equals", "less_than", "<", "=", ">"]:
            raise ValueError("Usage: comparison must be one of <, =, and >, or the text versions")

        #Handles the conversion from comparison input into valid SQL commands
        comparisonStr = None
        if comparison == "greater_than":
            comparisonStr = ">"
        elif comparison == "equals":
            comparisonStr = "="
        elif comparison == "less_than":
            comparisonStr = "<"
        else:
            comparisonStr = comparison

        #Compute the SQL command and return
        query = sql.SQL("{0} {1} %s").format(sql.Identifier(input_criterion),
                                          sql.Identifier(comparisonStr))

        queryString = query.as_string(self.connection).replace('"', "")

        query = self.cursor.mogrify(queryString, (compare_value,))

        return query

    def getAllMajorsRank(self):
        '''
        Returns a list of dictionaries containing all the majors we have data on, with ranks and nothing else.

        It returns: [{major: PETROLEUM ENGINEERING, rank: 1}, ............] (and so on and so forth for all majors)

        '''

        majorList = []
        #SQL command to get the dictionaries
        query = 'SELECT major, rank FROM majorsInformation'
        self.cursor.execute(query)

        #Gets all majors and their data
        for row in self.cursor:
            majorList.append(row)

        return majorList


    def findMajorByName(self, major_name):
        '''
        Return a dictionary with all of the information about the major with a given name.
        Throws a value error if the provided name isn't a valid major

        ex) findMajorByName("PETROLEUM ENGINEERING") returns
        {"rank": 1, "major_code": 2419, "major": "PETROLEUM ENGINEERING",
            "total": 2339, "men": 2057, "women:": 282, "major_category": "Engineering",
            "sharewomen": 0.120564344, "sample_size": 36, "employed": 1976,
            "full_time": 1849, "part_time":270, "full_time_year_round": 1207, "unemployed": 37,
            "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000, "p75th":125000,
            "college_jobs": 1534, "non_college_jobs":364, "low_wage_jobs":193}

        '''
        SpecificMajor = {}
        #SQL command to get one specific major
        query = 'SELECT * FROM majorsInformation WHERE major = %s'
        self.cursor.execute(query, (str(major_name),))


        for row in self.cursor:
            SpecificMajor = row
        #Error handling
        if SpecificMajor == {}:
            raise ValueError("Usage: There is no major with that name")

        return SpecificMajor

    def getAllMajorsData(self):
        '''
        Returns a list of dictionaries containing all the majors we have data on, each with all its data.

        It returns the equivalent of [{"rank": 1, "major_code": 2419, "major": "PETROLEUM ENGINEERING",
            "total": 2339, "men": 2057, "women:": 282, "major_category": "Engineering",
            "sharewomen": 0.120564344, "sample_size": 36, "employed": 1976,
            "full_time": 1849, "part_time":270, "full_time_year_round": 1207, "unemployed": 37,
            "unemployment_rate": 0.018380527, "median": 110000, "p25th": 95000, "p75th":125000,
            "college_jobs": 1534, "non_college_jobs":364, "low_wage_jobs":193},....] and so on
            for all 173 majors in the database
        '''
        majorList = []
        #SQL command to get all major dictionaries
        query = 'SELECT * FROM majorsInformation'
        self.cursor.execute(query)
        #Convert SQL to list
        for row in self.cursor:
            majorList.append(row)

        return majorList


    def sortMajorsBy(self, sort_tuples_list):
        '''
        Returns a byte string that represents a SQL query that takes in the list of tuples.
        We start with our query equal to "ORDER BY" then go through each tuple (which are written
        in the form (search_criterion, search_order) to append the extra
        ordering parameters. Throws a Value Error if the search_criterion or
        the search_order in any of the tuples aren't valid.

        ex) For sort_tuples_list of [("rank", "increasing")], we get the byte string:
        b"ORDER BY rank ASC"
        '''
        #Handle edge case
        if sort_tuples_list == []:
            return b""
        query = "ORDER BY "
        queryList = ["rank", "major", "major_category", "shareWomen", "unemployment_rate",
        "median", "p25th", "p75th"]
        for tuple in sort_tuples_list:
            #Error handling
            if tuple[0] not in queryList:
                raise ValueError("Usage: sort criterion must be a valid property of a major. You input " + tuple[0])
            if tuple[1] not in ["increasing", "decreasing", "ASC", "DESC", ""]:
                raise ValueError("Usage: direction must be empty or one of 'increasing' and 'decreasing'")
            #Create SQL code
            if tuple[1] in ("increasing", "ASC"):
                tuple = (tuple[0], "ASC")
            elif tuple[1] in ("decreasing", "DESC"):
                tuple = (tuple[0], "DESC")
            elif tuple[1] == "":
                tuple = (tuple[0], "DESC")
            query += "{0} {1}, "

            querySQL = sql.SQL(query).format(sql.Identifier(tuple[0]),
                                             sql.Identifier(tuple[1]))

            queryString = querySQL.as_string(self.connection).replace('"', "")

        query = bytes(queryString[:-2], 'utf-8')
        return query


    def filterAndSortMajors(self, list_of_filter_tuples, list_of_sort_tuples):
        '''
        Method that takes one list of tuples that contains everything the user wants to filter by (as done in filterMajorsBy)
        and one list of tuples that contains everything the user wants to sort by (as in sortMajorsBy).
        Using the filterMajorsBy and the sortMajorsBy methods, method then returns a list of all the
        majors which match the criteria in the input tuples, sorted in a desired fashion.

        ex) filterAndSortMajors([(major, =, 'PETROLEUM ENGINEERING')], [(major, "increasing")])
            will return:
            [{"rank": 1, "major_code": 2419, "major": "PETROLEUM ENGINEERING",
                "Total": 2339, "Men": 2057, "Women:": 282, "Major_category": "Engineering",
                "ShareWomen": 0.120564344, "Sample_size": 36, "Employed": 1976,
                "Full_time": 1849, "Part_time":270, "Full_time_year_round": 1207, "Unemployed": 37,
                "Unemployment_rate": 0.018380527, "Median": 110000, "P25th": 95000. "P75th":125000,
                "College_jobs": 1534, "Non_college_jobs":364, "Low_wage_jobs":193}]
        '''
        query = b"SELECT * FROM majorsInformation "
        if len(list_of_filter_tuples) != 0:
            query += b"WHERE "
        sortedAndFilteredList = []
        #Add each desired filter to the overall query
        for i in range(len(list_of_filter_tuples)):
            tuple = list_of_filter_tuples[i]
            query += self.filterMajorsBy(tuple[0], tuple[1], tuple[2])
            if i != len(list_of_filter_tuples)-1:
                query += b" AND "
        #Add each desired sort to the overall query
        query += self.sortMajorsBy(list_of_sort_tuples)
        query += b";"

        #Execute SQL and get the list of dictionaries with the desired params
        self.cursor.execute(query)
        for row in self.cursor:
            sortedAndFilteredList.append(row)

        return sortedAndFilteredList
