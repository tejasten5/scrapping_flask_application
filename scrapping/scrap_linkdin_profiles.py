from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os,csv,time,logging
from dotenv import load_dotenv
load_dotenv()
 
# create .env file with env variables.
# USER_EMAIL 
# USER_PASSWORD 
# IT Project Manager

'''
NOTE : optimization touchpts
1) Try to remove pagination number loop.(H)
2) Try to complete in O(n^3).(L)
3) Comple flask app (H)
'''




# DESIGNATIONS = ("CTO" ,"Director IT" , "VP IT" , "Head IT- (Technology)","Chief Information Security Officer","Exec Vice President - IT & Head Data",            
#                 "Head Apps: CRM and Contact Center Solution IT","Deputy Vice President, Engineering Head IT","IT Manager","IT Infra","IT Project Manager",    
#                 "Assistant Vice President - IT","IT Head (SAP)","IT Transformation Manager","Zonal Manager IT Infra - End User Technology",     
#                 "Vice President, Digital Technology Center","Senior Manager HR","Zonal HR Manager - AVP","Senior Manager HR")

                
                
                


class LinkdinHeaders:
    LD_FIRST_NAME = 'First Name'
    LD_LAST_NAME = 'Last Name'
    LD_COMPANY_NAME = 'Company Name'
    LD_DESIGNATIONS = 'Designation'
    LD_COUNTRIES = "Country"
    LD_CITIES = "City"
    LD_URLS = 'URL'

class ScrapLinkdinJobs:
    LINKDIN_LOGIN_URL = "https://linkedin.com/uas/login"
    FILE_NAME = "linkdin_profile.csv"
    NEW_FILE_NAME = "filter_profile.csv"
    TOTAL_RECORDS_ON_SINGLE_PAGE = 10
    global var_page
    var_page = 1

    HEADERS_LIST = [
        LinkdinHeaders.LD_FIRST_NAME,
        LinkdinHeaders.LD_LAST_NAME,
        LinkdinHeaders.LD_COMPANY_NAME,
        LinkdinHeaders.LD_DESIGNATIONS,
        LinkdinHeaders.LD_CITIES,
        LinkdinHeaders.LD_URLS        
    ]

    def __init__(self,company_name,post):
        print(post)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  
        self.DESIGNATIONS = post 
        self.COMPANIES =   company_name 

    def linkdin_login(self):  
        self.driver.get(self.LINKDIN_LOGIN_URL)
        time.sleep(5)

        soup=BeautifulSoup(self.driver.page_source, 'lxml')
        username = self.driver.find_element(By.ID,"username")
        username.send_keys(os.environ.get('USER_EMAIL'))

        pword = self.driver.find_element(By.ID,"password")
        pword.send_keys(os.environ.get('USER_PASSWORD'))		
        self.driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(3)

        self.scrap_linkdin_jobs()

        time.sleep(5)
        self.driver.close()
        
    def fetch_data(self,soup,dict_object,context):
        print("........")
        for html in soup.find(attrs={'class':'reusable-search__entity-result-list list-style-none'}).findAll(attrs={'class':'reusable-search__result-container'}):
            print("-----")
            try:
                profile_url = html.find(attrs={'class':'app-aware-link scale-down'})['href']
            except Exception as e:
                profile_url = "NA"

            try:
                name = html.findAll('span',attrs={'aria-hidden':'true'})[0].get_text()                        
                name_list = name.split()                                
                # fname,lname = name_list.pop(0)," ".join(name_list) if len(name_list) > 2 else name_list[0],name_list[1]
                if len(name_list) > 2:
                    fname,lname = name_list.pop(0)," ".join(name_list)                            
                else:
                    fname,lname = name_list[0],name_list[1]
            except Exception as e:
                fname = "NA"
                lname = "NA"
                            
            try:
                city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
            except Exception as e:
                city = "NA"

            try:
                designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
            except Exception as e:
                designation = "NA"


                context.update({
                    LinkdinHeaders.LD_FIRST_NAME:fname,
                    LinkdinHeaders.LD_LAST_NAME:lname,
                    LinkdinHeaders.LD_COMPANY_NAME:company[0],
                    LinkdinHeaders.LD_DESIGNATIONS:designation,
                    LinkdinHeaders.LD_CITIES:city,
                    LinkdinHeaders.LD_URLS:profile_url,
                    LinkdinHeaders.LD_COUNTRIES:""
                })                            
                dict_object.writerow(context) 

    def get_page(self,soup):
        li = []
        for val in soup.find(attrs={'class':'pb2 t-black--light t-14'}).get_text().strip('\n').split():
            if ',' in val:
                val = val.replace(',','')
                try:
                    val = int(val)
                except Exception as e:
                    val = None

                if val:
                    li.append(val)
        try:     
            total_records = li[0]
            page = round(total_records/self.TOTAL_RECORDS_ON_SINGLE_PAGE)
        except:
            page = 1
        return page
    
    def scrap_linkdin_jobs(self):
        unique_linkdin_profile_ids = set()     
        with open(self.FILE_NAME, "a") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=self.HEADERS_LIST)
            dict_object.writeheader()
            
            for company in self.COMPANIES:       
                for designation in self.DESIGNATIONS:
                    context = {}

                    url = '''https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{linkdin_company_code}%22%5D&keywords={company_name}&origin=FACETED_SEARCH&title={designation}
                    '''.format(linkdin_company_code = company[1],company_name=company[0],designation=designation.replace(' ','%20') if designation.isspace() else designation)
                        
                    self.driver.get(url)
                    time.sleep(60)

                    soup=BeautifulSoup(self.driver.page_source, 'html.parser')
                    

                    if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                        continue                     
                    
                    
                                         
                    var_page = self.get_page(soup)
                    for page_num in range(1,var_page+1):
                        
                        if page_num == 1:
                            url = url
                        else:        
                                               
                            url = url + '&page={page_number}'.format(page_number=page_num)
                        
                        self.driver.get(url)
                        soup=BeautifulSoup(self.driver.page_source, 'html.parser')
                    

                        if soup.find(attrs={'class':'reusable-search-filters__no-results artdeco-card mb2'}):
                            continue

                        for html in soup.find(attrs={'class':'reusable-search__entity-result-list list-style-none'}).findAll(attrs={'class':'reusable-search__result-container'}):
                            
                            try:
                                unique_profile_number = html.find(attrs={'class':'entity-result'})['data-chameleon-result-urn'].split(':')[-1]                                
                            except:
                                unique_profile_number = None

                            print(unique_profile_number,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",unique_profile_number not in unique_linkdin_profile_ids)

                            if unique_profile_number not in unique_linkdin_profile_ids:
                                try:
                                    profile_url = html.find(attrs={'class':'app-aware-link scale-down'})['href']
                                except Exception as e:
                                    profile_url = "NA"

                                try:
                                    name = html.findAll('span',attrs={'aria-hidden':'true'})[0].get_text()                        
                                    name_list = name.split()                                
                                    # fname,lname = name_list.pop(0)," ".join(name_list) if len(name_list) > 2 else name_list[0],name_list[1]
                                    if len(name_list) > 2:
                                        fname,lname = name_list.pop(0)," ".join(name_list)                            
                                    else:
                                        fname,lname = name_list[0],name_list[1]
                                except Exception as e:
                                    fname = "NA"
                                    lname = "NA"

                                try:
                                    designation = html.find(attrs={'class':'entity-result__primary-subtitle t-14 t-black t-normal'}).get_text().strip('\n')
                                except Exception as e:
                                    designation = "NA"

                                try:
                                    city = html.find(attrs = {'class':'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip('\n')
                                except Exception as e:
                                    city = "NA"

                                context.update({
                                    LinkdinHeaders.LD_FIRST_NAME:fname,
                                    LinkdinHeaders.LD_LAST_NAME:lname,
                                    LinkdinHeaders.LD_COMPANY_NAME:company[0],
                                    LinkdinHeaders.LD_DESIGNATIONS:designation,
                                    LinkdinHeaders.LD_CITIES:city,
                                    LinkdinHeaders.LD_URLS:profile_url,
                                })                            
                                dict_object.writerow(context)                            
                            
                                if unique_profile_number.isdigit():
                                        unique_linkdin_profile_ids.add(unique_profile_number)                                                                
                            time.sleep(10)
                            print("-----------------------------------------------------")                      
                time.sleep(10)
            time.sleep(10)
        time.sleep(10)
        
 

