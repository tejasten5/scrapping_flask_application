from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
import logging
import traceback




class CSVHeaders:
    CSV_DESIGNATION='Designation'
    CSV_COMPANY_NAME = 'Company Name'
    CSV_SALARY = 'Salary'
    CSV_EXPERIENCE = 'Experience'
    CSV_LOCATION = 'Location'
    CSV_ROLE = 'Role'
    CSV_SKILL = 'Skills'
    CSV_QUALIFICATION = 'Qualification'
    CSV_INDUSTRY_TYPE = 'Industry Type'
    CSV_FUNCTIONAL_AREA = 'Functional Area'
    CSV_EMPLOYMENT_TYPE = 'Employment Type'
    CSV_ROLE_CATEGORIE = 'Role Category'
    CSV_ADDRESS = 'Address'
    CSV_POST_BY = 'Post By'
    CSV_POST_DATE = 'Post Date'
    CSV_WEBSITE = 'Website'
    CSV_URL = 'Url'
    CSV_ABOUT_COMPANY = 'About Company'
    CSV_JOB_DESCRIPTION = 'Job Description'


class ScrapNaukriJobs(CSVHeaders):   

    BASE_URL = 'https://www.naukri.com/'
    FILE_NAME = 'scrap_naukri_jobs.csv'
    
    HEADERS_LIST = [
            CSVHeaders.CSV_DESIGNATION,
            CSVHeaders.CSV_COMPANY_NAME,
            CSVHeaders.CSV_SALARY,
            CSVHeaders.CSV_EXPERIENCE,
            CSVHeaders.CSV_LOCATION,
            CSVHeaders.CSV_ROLE,
            CSVHeaders.CSV_SKILL,
            CSVHeaders.CSV_QUALIFICATION,
            CSVHeaders.CSV_INDUSTRY_TYPE,
            CSVHeaders.CSV_FUNCTIONAL_AREA,
            CSVHeaders.CSV_EMPLOYMENT_TYPE,
            CSVHeaders.CSV_ROLE_CATEGORIE,
            CSVHeaders.CSV_ADDRESS,
            CSVHeaders.CSV_POST_BY,
            CSVHeaders.CSV_POST_DATE,
            CSVHeaders.CSV_WEBSITE,
            CSVHeaders.CSV_URL,
            CSVHeaders.CSV_ABOUT_COMPANY,
            CSVHeaders.CSV_JOB_DESCRIPTION,
        ]

    def __init__(self,language,ctc_string,city_string,industry_string):
        print(
            """                                         ________  ________     
                |\    |       /\      |        | |  /  |        |    |         
                | \   |      /  \     |        | | /   |________|    |         
                |  \  |     / -- \    |        | |/    |\            |         
                |   \ |    /      \   |        | |\    | \           |         
                |    \|   /        \  |________| | \   |  \       ___|____    
            ___________________________________________________________________
            """

        )
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.language = language.lower()
        self.CITY_FILTER_PARAMS = city_string
        self.CTC_FILTER_QUERY_PARAMS = ctc_string
        self.INDUSTRY_FILTER_PARAMS = industry_string
        self.job_detail_links = []

    def get_job_detail_links(self):
        print("Good to go..")
        for page in range(1,2):
            query_param = f'{self.language}-jobs'
            URL = URL = f"{self.BASE_URL}{query_param}?k={self.language}{self.CITY_FILTER_PARAMS}{self.CTC_FILTER_QUERY_PARAMS}{self.INDUSTRY_FILTER_PARAMS}" if page == 1 else f"{self.BASE_URL}{query_param}-{str(page)}?k={self.language}{self.CITY_FILTER_PARAMS}{self.CTC_FILTER_QUERY_PARAMS}{self.INDUSTRY_FILTER_PARAMS}"            
            self.driver.get(URL)            
            time.sleep(5) 
            soup=BeautifulSoup(self.driver.page_source, 'lxml')

            for outer_artical in soup.findAll(attrs={'class':"jobTuple bgWhite br4 mb-8"}):                
                for inner_links in outer_artical.find(attrs={'class':"jobTupleHeader"}).findAll(attrs={'class':"title fw500 ellipsis"}):
                    self.job_detail_links.append(inner_links.get('href'))

    def scrap_details(self):
        print("scrapping start..")
        self.get_job_detail_links()
        time.sleep(2)
        designation_list,company_name_list,experience_list,salary_list = [],[],[],[]        
        location_list,job_description_list,role_list,industry_type_list = [],[],[],[]        
        functional_area_list,employment_type_list,role_category_list,education_list = [],[],[],[]       
        key_skill_list,about_company_list,address_list,post_by_list = [],[],[],[]       
        post_date_list,website_list,url_list = [],[],[]  
        

        with open(self.FILE_NAME, 'a',encoding="utf-8") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=self.HEADERS_LIST)
            dict_object.writeheader()
            for link in range(len(self.job_detail_links)):
                context = {}
                time.sleep(10)
                self.driver.get(self.job_detail_links[link]) 
                soup=BeautifulSoup(self.driver.page_source, 'lxml')              
                

                if soup.find(attrs={'class':"salary"})==None: 
                    continue
                else:
                    context.update({self.CSV_DESIGNATION:"NA" if soup.find(attrs={'class':"jd-header-title"}) == None else soup.find(attrs={'class':"jd-header-title"}).text})
                    context.update({self.CSV_COMPANY_NAME:"NA" if soup.find(attrs={'class':"jd-header-comp-name"}) == None else soup.find(attrs={'class':"jd-header-comp-name"}).text})                    
                    context.update({self.CSV_SALARY:"NA" if soup.find(attrs={'class':"salary"})== None else soup.find(attrs={'class':"salary"}).text})
                    context.update({self.CSV_EXPERIENCE:"NA" if soup.find(attrs={'class':"exp"}) == None else soup.find(attrs={'class':"exp"}).text})
                    
                    loca = []
                    location=("NA" if soup.find(attrs={'class':'loc'}) == None else soup.find(attrs={'class':'loc'}).findAll('a'))
                    for i in location:
                        try:
                            loca.append(i.text)
                        except:
                            loca.append(["NA"])
                    context.update({self.CSV_LOCATION:",".join(loca)})

                    details=[]
                    try:
                        for i in soup.find(attrs={'class':"other-details"}).findAll(attrs={'class':"details"}):
                            details.append(i.text)
                            context.update({self.CSV_ROLE:details[0].replace('Role',''),
                            self.CSV_INDUSTRY_TYPE:details[1].replace('Industry Type',''),
                            self.CSV_FUNCTIONAL_AREA:details[2].replace('Functional Area',''),
                            self.CSV_EMPLOYMENT_TYPE:details[3].replace('Employment Type',''),
                            self.CSV_ROLE_CATEGORIE:details[4].replace('Role Category','')                
                        })
                    
                        context.update({self.CSV_JOB_DESCRIPTION:"NA" if soup.find(attrs={'class':"job-desc"})==None else soup.find(attrs={'class':"job-desc"}).text})
                        context.update({self.CSV_POST_DATE :["NA"] if soup.find(attrs={'class':"jd-stats"}) == None else [i for i in soup.find(attrs={'class':"jd-stats"})][0].text.split(':')[1]})

                        try:
                            context.update({self.CSV_WEBSITE:"NA" if soup.find(attrs={'class':"jd-header-comp-name"}).contents[0]['href'] == None else soup.find(attrs={'class':"jd-header-comp-name"}).contents[0]['href']})
                        except:
                            context.update({self.CSV_WEBSITE:"NA"})

                        try:    
                            context.update({self.CSV_URL:"NA" if soup.find(attrs={'class':"jd-header-comp-name"}) == None else soup.find(attrs={'class':"jd-header-comp-name"}).contents[0]['href']})
                        except:
                            context.update({self.CSV_WEBSITE:"NA"})
                       

                        qual=[]
                        for i in soup.find(attrs={'class':"education"}).findAll(attrs={'class':'details'}):
                            qual.append(i.text)
                        context.update({self.CSV_QUALIFICATION:qual}) 
                    

                        sk=[]
                        for i in soup.find(attrs={'class':"key-skill"}).findAll('a'):
                            sk.append(i.text)                     
                        context.update({self.CSV_SKILL:",".join(sk)})      

                        if soup.find(attrs={'class':"name-designation"})==None:
                            context.update({self.CSV_POST_BY:"NA"})         
                        else:
                            context.update({self.CSV_POST_BY:soup.find(attrs={'class':"name-designation"}).text})



                        if soup.find(attrs={'class':"about-company"})==None:                    
                            context.update({self.CSV_ABOUT_COMPANY:"NA"})
                        else:
                            context.update({self.CSV_ADDRESS:"NA" if soup.find(attrs={'class':"about-company"}).find(attrs={'class':"comp-info-detail"}) == None else soup.find(attrs={'class':"about-company"}).find(attrs={'class':"comp-info-detail"}).text})                      
                            context.update({self.CSV_ABOUT_COMPANY:soup.find(attrs={'class':"about-company"}).find(attrs={'class':"detail dang-inner-html"}).text})

                        dict_object.writerow(context)
                    except Exception as e:
                        print(traceback.format_exc())
                

        



