'''
api_tests.py
May 16th, 2019
By Daniel Kleber and Ginnie White

Code for all the unit tests that we wrote to test the functions of api.py.
These functions are purely for the API side of things and do not interact
with Flask or jinja.

'''
import api
import unittest
from decimal import *


class APITest(unittest.TestCase):

    testDict = None

    def setUp(self):
        getcontext().prec = 9
        shareWomen = Decimal(0.120564344).quantize(Decimal('.000000001'))
        unemployment_rate = Decimal(0.018380527).quantize(Decimal('.000000001'))
        self.testDict = {"rank": 1, "major_code": 2419, "major": "PETROLEUM ENGINEERING",
        "total": 2339, "men": 2057, "women": 282, "major_category": "Engineering",
        "sharewomen": shareWomen, "sample_size": 36, "employed": 1976,
        "full_time": 1849, "part_time":270, "full_time_year_round": 1207, "unemployed": 37,
        "unemployment_rate": unemployment_rate, "median": 110000, "p25th": 95000, "p75th":125000,
        "college_jobs": 1534, "non_college_jobs":364, "low_wage_jobs":193}
        self.API_checker = api.API()

    def tearDown(self):
        pass

    def test_rank_1(self):
        self.assertEqual(self.API_checker.findMajorByRank(1), self.testDict)

    def test_invalid_rank(self):
        self.assertRaises(ValueError, self.API_checker.findMajorByRank, 0)

    def test_filterMajorsBy_returns_bytes(self):
        query = self.API_checker.filterMajorsBy("unemployment_rate", "greater_than", "0.05")
        self.assertTrue(isinstance(query, bytes))

    def test_filterMajorsBy_filters(self):
        query = self.API_checker.filterMajorsBy("unemployment_rate", "greater_than", "0.05")
        self.assertEqual(query, b"unemployment_rate > '0.05'")

    def test_invalid_input_criterion(self):
       self.assertRaises(ValueError, self.API_checker.filterMajorsBy, "agent404", "greater_than", "0.05")

    def test_getAllMajorsRank_has_ranks(self):
        testMajor = self.API_checker.getAllMajorsRank()[0]
        self.assertTrue("rank" in testMajor)
        self.assertTrue("major" in testMajor)

    def test_getAllMajorsRank_does_not_have_unemployment_rate(self):
        testMajor = self.API_checker.getAllMajorsRank()[0]
        self.assertFalse("unemployment_rate" in testMajor)

    def test_getAllMajorsRank_has_correct_length(self):
        testMajor = self.API_checker.getAllMajorsRank()
        self.assertEqual(len(testMajor), 173)

    def test_petroleum_engineering(self):
        self.assertEqual(self.API_checker.findMajorByName("PETROLEUM ENGINEERING"), self.testDict)

    def test_invalid_name(self):
        self.assertRaises(ValueError, self.API_checker.findMajorByName,"Squiggledy Squeebley Sqack")

    def test_all_data_correct_number_of_elements(self):
        testList = self.API_checker.getAllMajorsData()
        self.assertEqual(len(testList), 173)

    def test_first_element_of_all_data(self):
        testMajor = self.API_checker.getAllMajorsData()[0]
        self.assertTrue("rank" in testMajor)
        self.assertTrue("unemployment_rate" in testMajor)
        self.assertTrue("median" in testMajor)
        self.assertTrue("major_category" in testMajor)

    def test_majors_sorted_has_invalid_input(self):
        self.assertRaises(ValueError, self.API_checker.sortMajorsBy, ("charisma", "increasing"))

    def test_majors_sorted_correctly_default(self):
        testQuery = self.API_checker.sortMajorsBy([("unemployment_rate", "")])
        self.assertEqual(testQuery, b"ORDER BY unemployment_rate DESC")

    def test_majors_sorted_correctly_increasing(self):
        testQuery = self.API_checker.sortMajorsBy([("unemployment_rate", "increasing")])
        self.assertEqual(testQuery, b"ORDER BY unemployment_rate ASC")

    def test_majors_sorted_correctly_decreasing(self):
        testQuery = self.API_checker.sortMajorsBy([("unemployment_rate", "decreasing")])
        self.assertEqual(testQuery, b"ORDER BY unemployment_rate DESC")

    def test_majors_sorted_handles_empty_list(self):
        self.assertEqual(self.API_checker.sortMajorsBy([]), b"")

    def test_filter_and_sort_has_correct_sort(self):
        test_filter_tuples = [('unemployment_rate', 'greater_than', '0.01'), ('median', 'greater_than', '50000')]
        test_sort_tuples = [('median', 'increasing')]
        testList = self.API_checker.filterAndSortMajors(test_filter_tuples, test_sort_tuples)
        testMajor1= testList[0]
        testMajor2 = testList [-1]
        self.assertTrue(testMajor1.get("median") <= testMajor2.get("median"))

    def test_filter_and_sort_filters_first(self):
        test_filter_tuples = [('unemployment_rate', 'greater_than', '0.01'), ('median', 'greater_than', '50000')]
        test_sort_tuples = [('median', 'increasing')]
        testList = self.API_checker.filterAndSortMajors(test_filter_tuples, test_sort_tuples)
        testMajor1= testList[0]
        testMajor2 = testList [-1]
        self.assertTrue(testMajor1.get("unemployment_rate") > 0.01)
        self.assertTrue(testMajor2.get("unemployment_rate") > 0.01)

    def test_filter_and_sort_filters_multiple(self):
        test_filter_tuples = [('unemployment_rate', 'greater_than', '0.01'), ('median', 'greater_than', '50000')]
        test_sort_tuples = [('median', 'increasing')]
        testList = self.API_checker.filterAndSortMajors(test_filter_tuples, test_sort_tuples)
        testMajor1= testList[0]
        testMajor2 = testList [-1]
        self.assertTrue(testMajor1.get("median") >= 50000)
        self.assertTrue(testMajor2.get("median") >= 50000)

    def test_filter_and_sort_throws_error(self):
        self.assertRaises(ValueError, self.API_checker.filterAndSortMajors, [('theyretaking','thehobbits','toIsengard')], [('nosesnoses','noses')])

if __name__ == '__main__':
    unittest.main()
