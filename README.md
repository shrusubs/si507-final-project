# si507-final-project

Project overview:
This program allows the user to scrape and crawl the Student Doctor Network (SDN) School Rankings site for information regarding the top 195 Medical Schools included in the SDN database

The user will start on the School Rankings Page for “All Medical Schools” (url included above), and will be scraping this page for each school’s name, year, city, state, and href link.

After obtaining each school’s unique href link, the user will crawl to the school’s individual page to extract additional school-related information, such as the school’s unique abbreviation, the year the school was founded, it's in state and out of state tuition rates, the school’s SDN-given ranking (scale of 1-5), the number of students enrolled in the most recent incoming class, and the average MCAT score and GPA of students who were most recently accepted and eventually matriculated to this school.

After adding this information to a database, the user will have the option of running several queries to obtain information such as geographical information about each school, the average MCAT score or GPAs for accepted students in the top 50 medical schools, the number and types of medical schools located in different US and Canada states, information about the medical schools located in a specific state searched for by the user, information on in-state and out-of-state tuition rates for the top 20 schools (or for a specific state), a breakdown of how many schools in the database are in each SDN-assigned rank level, and different combinations of such metrics for a specific state, country, or type of school they search. They will also have the option of obtaining a breakdown of allopathic vs osteopathic schools, in addition to other search criteria.

Data sources used:
Student Doctor Network's Medical School Rankings site:
https://schools.studentdoctor.net/schools/12/all-medical-s-schoolrankings/0?orderby=sdn_ranking&kwd=&sort_col=sdn_ranking&sort_dir=desc&psr=22&all=1&

Going to the above url will take you to the starting data source needed for running this program. This url is referred to as the "baseurl" in the code.

In addition to this baseurl, you will also need a plotly account to create the visualizations options provided in this code. You can follow the instructions at this link to set up an account and initialize the account into your terminal: https://plot.ly/python/getting-started/
^ Follow these instructions, skipping “Online Plot Privacy” and “Special Instructions for Plotly On-Premise Users.”

The program's code is organized as follows:
1 The MedSchool class organizes the attributes associated with each medical school.

2 The make_request_using_cache() function makes a request using caching to the baseurl to get the first set of information (href, school name, etc) from the SDN site.

3 The get_medschool_data() function uses the make_request_using_cache function to get the first set of information per school from the SDN site, and then uses the href link to crawl to each school's individual site to scrape for the second set of information

4 After this data is written to a csv file, the init_db and populate_db functions are called to create a medschool.db database will all of this information organized into two tables: School_Info and School_Stats.

5 Finally, the process_command function allows the user to enter various command/parameter combinations to obtain results regarding the medical schools based on their search criteria.

User Guide:

Commands available:

geo
  Description: Lists geographical info for medical schools according
  to the specified parameters.

  Options:
  * state=<name>|country=<name> [default: none]
    Description: Specifies a state or country within which to limit results.
    Country options are limited to USA, Canada, PuertoRico, and Singapore.
    States options are available for all US and select Canada states.

  * limit=<limit> [default: limit=20]
    Description: Specifies how many results to list.

performance
  Description: Lists medical school admission scores according to the specified
  parameters.

  Options:
  * state=<name>|country=<name> [default: none]
    Description: Specifies a state or country within which to limit results.
    Country options are limited to USA, Canada, PuertoRico, and Singapore.
    States options are available for all US and select Canada states.

  * type=<school type> [default: none]
    Description: Specifies a type of medical school (Allopathic or Osteopathic)
    within which to limit results.

  * rank=<number> [default: none]
    Description: Specifies whether to limit results to a specific SDN-given rank
    category (Rank value must be within the range of 1-5).

  * score=mcat|score=gpa [default: score=mcat]
    Description: Specifies what admission score to list in results.

  * top=<limit>|bottom=<limit> [default: top=10]
    Description: Specifies whether to list the top <limit> matches or the bottom
    <limit> matches. If Score is specified, the schools with the top <limit> or
    bottom <limit> scores is returned instead of by School Id.

  * OF NOTE: State parameter must be entered before either type or rank,
    and type must be entered before rank, if multiple parameters are entered.

tuition
  Description: Lists tuition information for medical schools according to the
  specified parameters.

  Options:
  * state=<name>|cost=<in>|cost<out> [default: cost=in]
    Description: Specifies whether to limit results by a certain state,
    or by In-state tuition or Out-of-state tuition. User can specify either
    a state, or In-state vs Out-of-state tuition results.

  * type=<school type> [default: none]
    Description: Specifies a type of medical school (Allopathic or Osteopathic)
    within which to limit results.

  * rank=<number> [default: none]
    Description: Specifies whether to limit results to a specific SDN-given rank
    category (Rank value must be within the range of 1-5).

  * top=<limit>|bottom=<limit> [default: top=10]
    Description: Specifies whether to list the top <limit> matches or the bottom
    <limit> matches. If Cost is specified, the schools with the top <limit> or
    bottom <limit> tuitions is returned instead of by School Id.

  * OF NOTE: State or Cost parameters must be entered before Type or Rank
    parameters, if multiple parameters are included.

numbers
  Description: Lists different counts of medical school attributes according to
  the specified parameters.

  Options:
  * rank|state|country|type [default: none]
    Description: Specifies that results should be limited to # of schools
    within each rank category, # of schools per state, # of schools per
    country, or # of schools per school type.

  * OF NOTE: One of the above 4 parameters MUST be entered along with the
    numbers command
