import unittest
from final_proj import *
import json
import requests

class TestDatabase(unittest.TestCase):

    def test_school_info_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        select = 'SELECT SchoolName FROM School_Info'
        results = cur.execute(select)
        results_list = results.fetchall()
        self.assertIn(('University of Michigan Medical School',), results_list)
        self.assertEqual(len(results_list), 195)

        sql_statement = '''
            SELECT Id, SchoolName, City, State, Type
            FROM School_Info
            WHERE Country="USA"
            ORDER BY State
        '''
        results = cur.execute(sql_statement)
        results_list = results.fetchall()
        self.assertEqual(len(results_list), 177)
        self.assertEqual(results_list[0][3], "AL")
        self.assertNotEqual(results_list[0][0], "1")

        conn.close()

    def test_school_stats_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        select = 'SELECT SchoolAbbrev FROM School_Stats'
        results = cur.execute(select)
        results_list = results.fetchall()
        self.assertEqual(len(results_list), 195)
        self.assertIn(('umich',), results_list)

        sql_statement = '''
            SELECT SchoolAbbrev, SDNRank, Enrolled, AvgMCAT, AvgGPA
            FROM School_Stats
            WHERE SDNRank="5"
        '''
        results = cur.execute(sql_statement)
        results_list = results.fetchall()
        self.assertEqual(len(results_list), 20)
        self.assertEqual(results_list[0][4], 3.6)
        self.assertEqual(results_list[13][3], 34.8)

        conn.close()

    def test_table_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql_statement = '''
            SELECT SchoolName, SDNRank, AvgGPA
            FROM School_Info
                JOIN School_Stats ON School_Info.Id = School_Stats.SchoolId
            WHERE State="MI"
        '''
        results = cur.execute(sql_statement)
        results_list = results.fetchall()
        self.assertIn(("University of Michigan Medical School", 5, 3.8), results_list)
        self.assertEqual(results_list[2][2], 3.8)

        conn.close()

class TestCommands(unittest.TestCase):

    def test_geo_search(self):
        results = process_command("geo limit=10")
        self.assertEqual(results[0][2], "Tulsa")

        results = process_command("geo country=Canada")
        self.assertEqual(results[0][1], "McGill University Faculty of Medicine")

    def test_performance_command(self):
        results = process_command("performance state=MI score=MCAT")
        self.assertEqual(results[1][1], 28.0)

        results = process_command("performance state=NY type=allopathic rank=4 bottom=5")
        self.assertEqual(results[0][0], "University of Rochester School of Medicine")

    def test_tuition_command(self):
        results = process_command("tuition rank=5")
        self.assertEqual(results[1][0], 22835)

    def test_numbers_command(self):
        results = process_command("numbers rank")
        self.assertEqual(results[1][0], 19)

        results = process_command("numbers country")
        self.assertEqual(results[0][1], "PuertoRico")

class TestMedSchoolInstance(unittest.TestCase):
    def test_constructor(self):
        medschool = MedSchool("University of Michigan Medical School", "umich", "1848", "177", "Allopathic", "Ann Arbor", "MI", "5", "32200", "51116", "34.8", "3.8")
        self.assertEqual(medschool.name, "University of Michigan Medical School")
        self.assertEqual(medschool.abbr, "umich")
        self.assertEqual(medschool.year, "1848")
        self.assertEqual(medschool.enrollment, "177")
        self.assertEqual(medschool.type, "Allopathic")
        self.assertEqual(medschool.city, "Ann Arbor")
        self.assertEqual(medschool.state, "MI")
        self.assertEqual(medschool.rank, "5")
        self.assertEqual(medschool.res_tuition, "32200")
        self.assertEqual(medschool.nonres_tuition, "51116")
        self.assertEqual(medschool.mcat, "34.8")
        self.assertEqual(medschool.gpa, "3.8")

    def test_string(self):
        medschool = MedSchool("University of Michigan Medical School", "umich", "1848", "177", "Allopathic", "Ann Arbor", "MI", "5", "32200", "51116", "34.8", "3.8")
        self.assertEqual(medschool.__str__(), "University of Michigan Medical School (1848, umich): 177 students enrolled, located in Ann Arbor, MI")

        # conn.close()

unittest.main()
