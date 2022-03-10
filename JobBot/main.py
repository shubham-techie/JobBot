# techie : Shubham Jaiswal

import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_colwidth',None)

def find_jobs():
    global familiar_skill

    # visiting "timesjobs.com" and getting html src code
    html_text = requests.get(
        f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={familiar_skill}&txtLocation=").text

    # parsing html src code
    soup = BeautifulSoup(markup=html_text, features='lxml')

    # finding all jobs of all skills
    jobs = soup.find_all(name='li', class_="clearfix job-bx wht-shd-bx")

    # creating lists to store
    company = []
    skills_list = []
    more_info_link = []
    job_dict = {'Company': company,
                'Skills': skills_list,
                'More info': more_info_link
                }

    i = 0  # counter to keep record of jobs in a single file

    print('Filtering out..............')

    for job in jobs:
        posted_date = job.find('span', class_="sim-posted").span.text

        # looking for the jobs which are posted recently
        if 'few' in posted_date:
            skills = job.find('span', class_='srp-skills').text.strip().split(',')
            skills = list(map(lambda skill: skill.strip().lower(), skills))

            if familiar_skill in skills:
                i += 1
                company_name = job.find('h3', class_="joblist-comp-name").text.strip()
                more_info = job.header.h2.a['href']

                # making lists so that further we can make dataframe
                company.append(company_name)
                skills_list.append(skills)
                more_info_link.append(more_info)

    jobs = pd.DataFrame(job_dict)
    # print(jobs)

    # saving the file
    if i > 0:
        os.makedirs("./jobs", exist_ok=True)  # creates jobs directory

        FILE_NAME = familiar_skill + '_job' + str(FILE_NO) + '.csv'
        jobs.to_csv('./jobs/' + FILE_NAME)

        print(f'File saved : {i} jobs available in {FILE_NAME}')
    else:
        print(f'Currently no jobs are available for  {familiar_skill}.')
        print('Please look for another skill')

        familiar_skill = input('\nWhat skill you have?\n > ').lower()  # taking input of skill
        print(f'Looking for {familiar_skill.upper()} jobs..........')
        find_jobs()


# driver function
if __name__ == '__main__':
    '''Every 10 mins .......
    Finds all the available jobs having your required skill and 
    saves the companyName and descriptionOfJob in csv file
    '''

    familiar_skill = input('What skill you have?\n > ').lower()  # taking input of skill
    FILE_NO = 0  # count of job file in every 10 mins

    # looping infinitely to scrap the jobs from 'timesjobs.com' in every 10 mins
    while True:
        print(f'Looking for {familiar_skill.upper()} jobs..........')
        FILE_NO += 1
        find_jobs()

        time_wait = 10  # in minutes
        print(f'Waiting {time_wait} minutes.......')
        time.sleep(time_wait * 60)
        print()
