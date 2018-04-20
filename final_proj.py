# SI 507 Final Project Code
# Scraping and Crawling the Student Doctor Network site for Information on North American Medical Schools

# SDN All Medical Schools

import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import csv
from prettytable import PrettyTable
import plotly.plotly as py
import plotly.graph_objs as go

class MedSchool():
    def __init__(self, name, abbr, year, enrollment, type, city, state, rank, res_tuition, nonres_tuition, mcat, gpa):
        self.name = name
        self.abbr = abbr
        self.year = year
        self.enrollment = enrollment
        self.type = type
        self.city = city
        self.state = state
        self.rank = rank
        self.res_tuition = res_tuition
        self.nonres_tuition = nonres_tuition
        self.mcat = mcat
        self.gpa = gpa

    def __str__(self):
        return "{} ({}, {}): {} students enrolled, located in {}, {}".format(self.name, self.year, self.abbr, self.enrollment, self.city, self.state)

# medschool = MedSchool("University of Michigan Medical School", "umich", "1848", "177", "Allopathic", "Ann Arbor", "MI", "5", "32200", "51116", "34.8", "3.8")
# print(medschool.__str__())

CACHE_FNAME = "sdn_medschool_cache.json"
try:
	f = open(CACHE_FNAME, "r")			#CREATING CACHE FILE
	fstr = f.read()
	CACHE_DICTION = json.loads(fstr)
	f.close()
except:
	CACHE_DICTION = {}

def get_unique_key(baseurl):
    return baseurl

def make_request_using_cache(baseurl):
    global header
    unique_ident = get_unique_key(baseurl)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# baseurl = 'https://schools.studentdoctor.net/schools/12/all-medical-s-school-rankings/0'

baseurl = 'https://schools.studentdoctor.net/schools/12/all-medical-s-school-rankings/0?orderby=sdn_ranking&kwd=&sort_col=sdn_ranking&sort_dir=desc&psr=22&all=1&'


def get_medschool_data(baseurl):
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
# print(page_soup.prettify())
    content_div = page_soup.find(class_ = 'row doc-content content')
    table_rows = content_div.find_all('tr')

    href_links_list = []
    medschool_abbr_list = []
    medschool_names_list = []
    # medschool_location_list = []
    counter = 0

    medical_schools_list = []

    for i in range(2,197): # 2-197
        all_med_schools = table_rows[i].find_all('a')
        # print(all_med_schools[1])
        # link = all_med_schools[1].split('"')
        abbr = all_med_schools[0]['name']
        medschool_abbr_list.append(abbr)
        school_link = all_med_schools[1]['href']
        href_links_list.append(school_link)
        # print(school_link)
        name = all_med_schools[1].string
        if "(" in name:
            split_name = name.split("(")
            name = split_name[0][:-1]
            # print(name)

        if "Long School" in name:
            split_name = name.split(",")
            name = split_name[0]
            # print('"' + name + '"')
            # name = split_name[0]
        medschool_names_list.append(name)
        # print(medschool_names_list)
        # print(school_name)
        school_type = table_rows[i].find_all('dd')[0].string
        type = school_type.split(" ")[0]
        # print(type)
        location = table_rows[i].find_all('dd')[1].string[1:-1]
        if location == '':
            city = ''
            state = ''
        if "," in location:
            split_location = location.split(",")
            city = split_location[0].strip()
            state = split_location[1][1:]
        else:
            city = location
            state = ''

        counter += 1
        print(counter)
        # medschool_links = get_medschool_data(baseurl)
        sdn_rankings_list = []
        # print(medschool_links)


    # for link in href_links_list[:3]:
        baseurl2 = 'https://schools.studentdoctor.net'
        school_url = baseurl2 + school_link

        school_info_text = make_request_using_cache(school_url)
        school_info_soup = BeautifulSoup(school_info_text, 'html.parser')
        # school_content_div = school_info_soup.find(class_ = 'medium-12 large-8 columns')
        content_ul = school_info_soup.find('ul', {"class": "graph-list no-bullet"})
        content_li = content_ul.find_all('li') # ***** changed to find_all

        content_ul2 = school_info_soup.find('ul', {'class': "meta-list no-bullet"})
        content_li2 = content_ul2.find_all('li')

        content_ul3 = school_info_soup.find('ul', {'class': "section-list three-col stats-overall no-bullet cf"})
        content_li3 = content_ul3.find_all('li')

        content_ul4 = school_info_soup.find_all('ul', {'class': "section-list three-col stats-overall no-bullet cf"})[1]
        content_li4 = content_ul4.find_all('li')

        try:
            rank = content_li[0].text.strip().split("\n")[1]
            if rank == "-":
                rank = ''
            # print(rank)
            # rank = content_li.find("span", {'class': 'graph-circle green five'}).text # Original
            year = content_li2[0].text[14:]
            enrollment = content_li2[1].text[16:]
            if enrollment[-1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                enrollment = ''
            # if content_li2[1].text == 'View Site >':
            #     enrollment = ''
            res_tuition = content_li3[0].text.strip().split("\n")[1][1:].replace(",", "")
            nonres_tuition = content_li3[1].text.strip().split("\n")[1][1:].replace(",", "")
            mcat = content_li4[0].text.strip().split('\n')[1]
            if mcat == '-':
                mcat = ''
            gpa = content_li4[1].text.strip().split('\n')[1]
            if gpa == '-':
                gpa = ''

        except:
            rank = ''
            year = ''
            enrollment = ''
            res_tuition = ''
            nonres_tuition = ''
            mcat = ''
            gpa = ''

        med_school_instance = MedSchool(name=name, abbr=abbr, year=year, enrollment=enrollment, type=type, city=city, state=state, rank=rank, res_tuition=res_tuition, nonres_tuition=nonres_tuition, mcat=mcat, gpa=gpa)

        medical_schools_list.append(med_school_instance)
    # print(medical_schools_list)

    return medical_schools_list

# get_medschool_data(baseurl)

us_states_list = ['AL', 'AZ', 'AK', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

canada_list = ['AB', 'BC', 'MB', 'NS', 'ON', 'QC', 'SK']

puerto_rico = ['PR']

def create_csv(medical_schools_list):
    medschool_file = open("medical_schools.csv", "w")
    medschool_file.write("SchoolName, SchoolAbbrev, Year, Enrolled, City, State, Country, SDNRank, ResTuition, NonResTuition, AvgMCAT, AvgGPA, Type\n")

    for medschool in medical_schools_list:
        SchoolName = medschool.name
        SchoolAbbrev = medschool.abbr
        Year = medschool.year
        Enrolled = medschool.enrollment
        City = medschool.city
        State = medschool.state
        if State.upper() in us_states_list:
            Country = 'USA'
        elif State.upper() in canada_list:
            Country = 'Canada'
        elif State.upper() in puerto_rico:
            Country = 'PuertoRico'
        else:
            Country = 'Singapore'
        SDNRank = medschool.rank
        ResTuition = medschool.res_tuition
        NonResTuition = medschool.nonres_tuition
        AvgMCAT = medschool.mcat
        AvgGPA = medschool.gpa
        Type = medschool.type
        medschool_file.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(SchoolName, SchoolAbbrev, Year, Enrolled, City, State, Country, SDNRank, ResTuition, NonResTuition, AvgMCAT, AvgGPA, Type))
    medschool_file.close()

# create_csv(get_medschool_data(baseurl))
#___________________________________________#

DBNAME = 'medschools.db'
MEDCSV = 'medical_schools.csv'

def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Exception as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'School_Info'
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'School_Info' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'SchoolName' TEXT NOT NULL,
        'Year' INTEGER,
        'City' TEXT,
        'State' TEXT,
        'Country' TEXT,
        'ResTuition' INTEGER,
        'NonResTuition' INTEGER,
        'Type' TEXT NOT NULL
    );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'School_Stats';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'School_Stats' (
        'SchoolAbbrev' TEXT PRIMARY KEY,
        'SchoolId' INTEGER,
        'SDNRank' INTEGER,
        'Enrolled' INTEGER,
        'AvgMCAT' REAL,
        'AvgGPA' REAL,
        FOREIGN KEY (SchoolId) REFERENCES School_Info(Id)
    );
    '''
    cur.execute(statement)
    conn.commit()

init_db()

def populate_medschool_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    f = open(MEDCSV, 'r')
    csv_data = csv.reader(f)
    csv_list = list(csv_data)
    del(csv_list[0])

    for row in csv_list:
        insertion = (None, row[0], row[2], row[4], row[5], row[6], row[8], row[9], row[12])
        statement = 'INSERT INTO "School_Info" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()
    # print(medschool_id_dict)
    medschool_id_dict = {}
    id = 1
    for row in csv_list:
        insertion = (row[1], None, row[7], row[3], row[10], row[11])
        statement = 'INSERT INTO "School_Stats" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'
        medschool_id_dict[row[1]] = id
        id += 1
        cur.execute(statement, insertion)
    conn.commit()

    for key in medschool_id_dict:
        try:
            statement = 'UPDATE School_Stats SET SchoolId = ' + str(medschool_id_dict[key]) + ' WHERE SchoolAbbrev = "' + key + '"'
            cur.execute(statement)
            conn.commit()
        except:
            pass

populate_medschool_db()


def geo_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_st = 'SELECT Id, SchoolName, City, State, Country, Type '
    from_st = 'FROM School_Info '
    join = ''
    location_state = ''
    country = ''
    school_type = ''
    order_by = 'ORDER BY Id, Type '
    top_bottom1 = ''
    top_bottom2 = 'LIMIT 20'

    command_space_split = command.split(" ")
    state_exists = False
    for param in command_space_split:
        if "state" in param:
            state_exists = True
            state_split_value = param.split("=")
            state_value = state_split_value[1].upper()
            location_state = 'WHERE State = "' + state_value + '" '


        if "country" in param:
            state_exists = True
            country_value = param.split("=")[1]
            if country_value.upper() == "USA":
                country = 'WHERE Country = "USA" '
            if country_value.lower() == "canada":
                country = 'WHERE Country = "Canada" '
            if country_value.lower() == "puertorico":
                country = 'WHERE Country = "PuertoRico" '

        # if "type" in param:
        #     if state_exists:
        #         type_value = param.split("=")[1].title()
        #         school_type = 'AND Type = "' + type_value + '" '
        #     else:
        #         type_value = param.split("=")[1].title()
        #         school_type = 'WHERE Type = "' + type_value + '" '

        if "limit" in param:
            limit_value = param.split("=")[1]
            top_bottom2 = 'LIMIT ' + limit_value

    statement = select_st + from_st + join + location_state + country + school_type + order_by + top_bottom1 + top_bottom2
    # print(statement)
    cur.execute(statement)
    data_list = []
    x = PrettyTable()
    x.field_names = ["Id", "SchoolName", "City", "State", "Country", "SchoolType"]
    for row in cur:
        x.add_row(row)
        data_list.append(row)
    print(x)
    return data_list

# geo_command("geo state=mi limit=7")

def performance_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_st = 'SELECT si.Id, si.SchoolName, si.State, si.Country, si.Type, ss.SDNRank, ss.AvgMCAT '
    from_st = 'FROM School_Info as si '
    join = 'JOIN School_Stats as ss ON si.Id = ss.SchoolId '
    location_state = ''
    country = ''
    school_type = ''
    rank = ''
    score = ''
    order_by = 'ORDER BY Id, Type, SDNRank '
    top_bottom1 = 'DESC '
    top_bottom2 = 'LIMIT 10'

    command_space_split = command.split(" ")
    state_exists = False
    type_exists = False
    score_exists = False
    for param in command_space_split:
        if "state" in param:
            state_exists = True
            state_split_value = param.split("=")
            state_value = state_split_value[1].upper()
            # if state_value in us_states_list:
            location_state = 'WHERE State = "' + state_value + '" '

        if "country" in param:
            state_exists = True
            country_value = param.split("=")[1]
            if country_value.upper() == "USA":
                country = 'WHERE Country = "USA" '
            if country_value.lower() == "canada":
                country = 'WHERE Country = "Canada" '
            if country_value.lower() == "puertorico":
                country = 'WHERE Country = "PuertoRico" '

        if "type" in param:
            type_exists = True
            if state_exists:
                type_value = param.split("=")[1].title()
                school_type = 'AND Type = "' + type_value + '" '
            else:
                type_value = param.split("=")[1].title()
                school_type = 'WHERE Type = "' + type_value + '" '

        if "rank" in param:
            if state_exists:
                rank_value = param.split("=")[1]
                rank = 'AND ss.SDNRank = "' + rank_value + '" '
            elif type_exists:
                rank_value = param.split("=")[1]
                rank = 'AND ss.SDNRank = "' + rank_value + '" '
            else:
                rank_value = param.split("=")[1]
                rank = 'WHERE ss.SDNRank = "' + rank_value + '" '

        if "score" in param:
            score_exists = True
            # if state_exists:
            score_value = param.split("=")[1]
            if score_value.lower() == "gpa":
                select_st = 'SELECT si.Id, si.SchoolName, si.State, si.Country, si.Type, ss.SDNRank, ss.AvgGPA '

        if "top" in param:
            top_value = param.split("=")[1]
            if score_exists:
                if score_value.lower() == "gpa":
                    order_by = 'ORDER BY ss.AvgGPA '
                    top_bottom1 = 'DESC '
                    top_bottom2 = 'LIMIT ' + top_value
                else:
                    order_by = 'ORDER BY ss.AvgMCAT '
                    top_bottom1 = 'DESC '
                    top_bottom2 = 'LIMIT ' + top_value
            else:
                order_by = 'ORDER BY SchoolId '
                top_bottom1 = ''
                top_bottom2 = 'LIMIT ' + top_value

        if "bottom" in param:
            limit_value = param.split("=")[1]
            if score_exists:
                if score_value.lower() == "gpa":
                    order_by = 'ORDER BY ss.AvgGPA '
                    top_bottom1 = ''
                    top_bottom2 = 'LIMIT ' + limit_value
                else:
                    order_by = 'ORDER BY ss.AvgMCAT '
                    top_bottom1 = ''
                    top_bottom2 = 'LIMIT ' + limit_value
            else:
                order_by = 'ORDER BY SchoolId '
                top_bottom1 = 'DESC '
                top_bottom2 = 'LIMIT ' + limit_value

    statement = select_st + from_st + join + location_state + country + school_type + rank + score + order_by + top_bottom1 + top_bottom2
    # print(statement)
    school_list = []
    scores_list = []
    data_list = []
    cur.execute(statement)
    x = PrettyTable()
    x.field_names = ["Id", "SchoolName", "State", "Country", "SchoolType", "SDN_Rank", "MCAT/GPA"]
    for row in cur:
        x.add_row(row)
        school_list.append(row[1])
        scores_list.append(row[6])
    # print(school_list)
    # print(scores_list)
    data_list.append(school_list)
    data_list.append(scores_list)
    print(x)
    return data_list

# print(performance_command("performance rank=4 top=10 score=mcat"))

def tuition_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_st = 'SELECT Id, SchoolName, City, State, ResTuition, Type, ss.SDNRank '
    from_st = 'FROM School_Info '
    join = 'JOIN School_Stats as ss ON School_Info.Id = ss.SchoolId '
    location_state = ''
    country = 'WHERE Country <> "Canada" AND Country <> "PuertoRico" AND Country <> "Singapore" AND ResTuition <> "" '
    school_type = ''
    rank = ''
    order_by = 'ORDER BY Id, Type, ss.SDNRank '
    top_bottom1 = 'DESC '
    top_bottom2 = 'LIMIT 10'

    command_space_split = command.split(" ")
    state_exists = False
    type_exists = False
    cost_exists = True
    for param in command_space_split:
        if "state" in param:
            state_exists = True
            state_split_value = param.split("=")
            state_value = state_split_value[1].upper()
            location_state = 'WHERE State = "' + state_value + '" '
            country = ''

        if "cost" in param:
            cost_exists = False
            cost_value = param.split("=")[1].lower()
            if cost_value == "out":
                select_st = 'SELECT Id, SchoolName, City, State, NonResTuition, Type, ss.SDNRank '
                country = 'WHERE Country <> "Canada" AND Country <> "PuertoRico" AND Country <> "Singapore" AND NonResTuition <> "" '
                order_by = 'ORDER BY Type, NonResTuition '
            if cost_value == "in":
                order_by = 'ORDER BY Type, ResTuition '

        if "type" in param:
            type_exists = True
            # if state_exists:
            type_value = param.split("=")[1].title()
            school_type = 'AND Type = "' + type_value + '" '

        if "rank" in param:
            # if state_exists:
            rank_value = param.split("=")[1]
            rank = 'AND ss.SDNRank = "' + rank_value + '" '

        if "top" in param:
            if cost_exists:
                top_value = param.split("=")[1]
                top_bottom2 = 'LIMIT ' + top_value
                order_by = 'ORDER BY Type, ResTuition '
            else:
                top_value = param.split("=")[1]
                top_bottom2 = 'LIMIT ' + top_value

        if "bottom" in param:
            if cost_exists:
                bottom_value = param.split("=")[1]
                top_bottom1 = ''
                top_bottom2 = 'LIMIT ' + bottom_value
                order_by = 'ORDER BY Type, ResTuition '
            else:
                bottom_value = param.split("=")[1]
                top_bottom1 = ''
                top_bottom2 = 'LIMIT ' + bottom_value

    statement = select_st + from_st + join + location_state + country + school_type + rank + order_by + top_bottom1 + top_bottom2
    # print(statement)
    cur.execute(statement)
    school_names_list = []
    tuition_list = []
    data_list = []
    x = PrettyTable()
    x.field_names = ["Id", "SchoolName", "City", "State", "In/Out($)", "Type", "SDNRank"]
    for row in cur:
        x.add_row(row)
        school_names_list.append(row[1])
        tuition_list.append(row[4])
    data_list.append(school_names_list)
    data_list.append(tuition_list)
    # print(data_list)
    print(x)
    return data_list

# tuition_command("tuition cost=out")
# performance_command("performance country=us top=15 score=mcat")

def numbers_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_st = 'SELECT COUNT(*) '
    from_st = 'FROM School_Info as si '
    join = 'JOIN School_Stats as ss ON si.Id = ss.SchoolId '
    location_state = ''
    country = ''
    school_type = ''
    rank = ''
    group_by = ''
    # top_bottom1 = 'DESC '
    # top_bottom2 = 'LIMIT 10'
    command_space_split = command.split(" ")
    for param in command_space_split:
        if "rank" in param:
            if "=" in param:
                select_st = 'SELECT ss.SDNRank, COUNT(*) '
                rank_value = param.split("=")[1]
                rank = 'WHERE ss.SDNRank = "' + rank_value + '" '
            else:
                select_st = 'SELECT ss.SDNRank, COUNT(*) '
                group_by = 'GROUP BY ss.SDNRank'
                # INSERT OPTION FOR BAR GRAPH OF # SCHOOLS PER RANK HERE

        if "type" in param:
            if "=" in param:
                type_value = param.split("=")[1].title()
                select_st = 'SELECT si.Type, COUNT(*) '
                school_type = 'WHERE si.Type = "' + type_value + '" '
            else:
                select_st = 'SELECT si.Type, COUNT(*) '
                group_by = 'GROUP BY si.Type'
                # INSERT OPTION FOR PIE CHART OF % ALLOPATHIC VS % OSTEOPATHIC HERE

        if "country" in param:
            if "=" in param:
                select_st = 'SELECT si.Country, COUNT(*) '
                country_value = param.split("=")[1]
                if country_value.upper() == "USA":
                    country = 'WHERE Country = "USA" '
                if country_value.lower() == "canada":
                    country = 'WHERE Country = "Canada" '
                if country_value.lower() == "puertorico":
                    country = 'WHERE Country = "PuertoRico" '
            else:
                select_st = 'SELECT si.Country, COUNT(*) '
                group_by = 'GROUP BY si.Country'

        if "state" in param:
            if "=" in param:
                state_split_value = param.split("=")
                state_value = state_split_value[1].upper()
                select_st = 'SELECT si.State, COUNT(*) '
                location_state = 'WHERE State = "' + state_value + '" '
            else:
                select_st = 'SELECT si.State, COUNT(*) '
                group_by = 'GROUP BY si.State'

    statement = select_st + from_st + join + location_state + country + school_type + rank + group_by
    # print(statement)
    cur.execute(statement)
    param_list = []
    param_value_list = []
    data_list = []
    x = PrettyTable()
    x.field_names = ["Rank/Type/State/Country", "Count"]
    for row in cur:
        x.add_row(row)
        param_list.append(row[0])
        param_value_list.append(row[1])
    data_list.append(param_list)
    data_list.append(param_value_list)
    print(x)
    return data_list

# numbers_command("numbers rank")

def plot_scores(data_list):
    x = data_list[0]
    y = data_list[1]

    data = [go.Bar(
                x=x,
                y=y,
                text=y,
                textposition = 'auto',
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5),
                ),
                opacity=0.6
            )]

    py.plot(data, filename='school-scores-distribution')

    return None

# plot_scores(performance_command("performance top=15 score=gpa"))

def plot_tuition(data_list):
    trace = go.Scatter(
    x = data_list[0],
    y = data_list[1],
    mode = 'markers'
    )

    data = [trace]

    py.plot(data, filename='school-tuitions')
    return None

# plot_tuition(tuition_command("tuition cost=in bottom=15"))

def plot_ranks(data_list):
    trace1 = go.Bar(
    y=['Rank'],
    x= data_list[1][0],
    name='SDN_Rank = 1',
    orientation = 'h',
    marker = dict(
        color = 'red',
        line = dict(
            color = 'red',
            width = 3)
        )
    )
    trace2 = go.Bar(
        y=['Rank'],
        x=data_list[1][1],
        name='SDN_Rank = 2',
        orientation = 'h',
        marker = dict(
            color = 'orange',
            line = dict(
                color = 'orange',
                width = 3)
        )
    )
    trace3 = go.Bar(
        y=['Rank'],
        x=data_list[1][2],
        name='SDN_Rank = 3',
        orientation = 'h',
        marker = dict(
            color = 'yellow',
            line = dict(
                color = 'yellow',
                width = 3)
        )
    )

    trace4 = go.Bar(
        y=['Rank'],
        x=data_list[1][3],
        name='SDN_Rank = 4',
        orientation = 'h',
        marker = dict(
            color = 'green',
            line = dict(
                color = 'green',
                width = 3)
        )
    )

    trace5 = go.Bar(
        y=['Rank'],
        x=data_list[1][4],
        name='SDN_Rank = 5',
        orientation = 'h',
        marker = dict(
            color = 'blue',
            line = dict(
                color = 'blue',
                width = 3)
        )
    )

    data = [trace1, trace2, trace3, trace4, trace5]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='school-rankings')

    return None

# plot_ranks(numbers_command("numbers rank"))

def plot_school_type(data_list):
    labels = data_list[0]
    values = data_list[1]

    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='school_type_pie_chart')

# plot_school_type(numbers_command("numbers country"))

def process_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    commands_list = ["geo", "performance", "tuition", "numbers"]

    if command.split()[0] == "geo":
        return geo_command(command)

    elif command.split()[0] == "performance":
        return performance_command(command)

    elif command.split()[0] == "tuition":
        return tuition_command(command)

    elif command.split()[0] == "numbers":
        return numbers_command(command)

    elif command.split()[0] not in commands_list:
        print("Command not recognized: " + command)

def load_help_text():
    with open('help.txt') as f:
        return f.read()

command_params_list = ["state", "country", "limit", "rank", "score", "type", "top", "bottom", "cost"]

def interactive_prompt():
    help_text = load_help_text()
    commands_list = []
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

        elif response == '':
            continue

        elif response == 'exit':
            print("bye!")
            break

        else:
            response_space_split = response.split(" ")
            if len(response_space_split) >= 2:
                bad_command = False
                for i in range(1, len(response_space_split)):
                    if "=" not in response_space_split[i]:
                        if response_space_split[i] not in command_params_list:
                            print("Command not recognized: " + response)
                            bad_command = True
                            break
                    else:
                        response_equal_split = response_space_split[i].split("=")
                        if response_equal_split[0] not in command_params_list:
                            print("Command not reconized: " + response)
                            bad_command = True
                            break
                if bad_command:
                    continue
        process_command(response)
        response_space_split = response.split(" ")
        if response_space_split[0] != "geo":
            plot_response = input("Would you like to visualize this data? ")
            if plot_response == 'yes':
                if response_space_split[0] == "performance":
                    output = performance_command(response)
                    plot_scores(output)
                elif response_space_split[0] == "tuition":
                    output = tuition_command(response)
                    plot_tuition(output)
                elif response_space_split[0] == "numbers":
                    if response_space_split[1] == "rank":
                        output = numbers_command(response)
                        plot_ranks(output)
                    if response_space_split[1] == "type" or response_space_split[1] == "state" or response_space_split[1] == "country":
                        output = numbers_command(response)
                        plot_school_type(output)
                elif response_space_split[0] not in commands_list:
                    print("I'm sorry, that is not a valid command. Please start over.")
                continue

            elif plot_response == 'no':
                continue

            elif plot_response == 'help':
                print(help_text)
                continue

            elif plot_response == 'exit':
                print("bye!")
                break
            # else:
            #     print("I'm sorry, that is not a valid option. Please start over. ")


if __name__=="__main__":
    interactive_prompt()
    # pass
# plot_school_type(numbers_command("numbers type"))
# Plotly graphs:

# Bar graph of the number of schools within each SDN Rank category
# Scatterplot of the average GPA for number of medical schools specified
# Histogram of the average MCAT scores for top number of schools specified
# Two-level bar graph comparing resident and non-resident tuitions for number of schools specified
# Pie Chart of percentage of schools that are allopathic vs osteopathic





# plot_school_ranks()



# are you getting data from api
# is this data correct
# test the formatting --> if you requested 10 things, did you get 10 things back
# testing json file for dictionary keys
# if loading database, does DB have the correct type of data --> testing queries
    # queries that should and should not be getting output



#_________________________end_________________________#
