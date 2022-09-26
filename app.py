from flask import (Flask,render_template,url_for,request,redirect,jsonify)
from utils import constant,cust_response
from scrapping import ScrapNaukriJobs,ScrapLinkdinJobs
import logging,time
import traceback


app = Flask(__name__)
app.config['SECREAT_KEY'] = "NE0$0FT@123"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == "POST":        
        platform_id = request.form.get('platform')
        

        if platform_id == '1':
            routing_path = 'linkdin'
        elif platform_id == '2':
            routing_path = 'naukri'
        else:
            routing_path = 'linkdin-jobs'

        return redirect(routing_path)
    return render_template('home.html')


@app.route('/scrap-naukri',methods=["POST"])
def scrap_naukri_jobs():
    

    try:
        if request.method == "POST": 
            language = request.form.get('language')
            salary_filter = request.form.get('salary_filter')
            city_filter = request.form.get('city_filter')
            industry_filter = request.form.get('industry_filter')

            if not language:
                return jsonify(cust_response(success = False,message="Programming language required.",status_code=400))
        
            if not salary_filter:
                return jsonify(cust_response(success = False,message="Salary required.",status_code=400))

            if not city_filter:
                return jsonify(cust_response(success = False,message="City required.",status_code=400))

            if not industry_filter:
                return jsonify(cust_response(success = False,message="Industry required.",status_code=400))

            if salary_filter.endswith(','):
                salaries = salary_filter.split(',')
                salaries.pop()

            
            if city_filter.endswith(','):
                _cities = city_filter.split(',')
                _cities.pop()

            
            if industry_filter.endswith(','):
                industries = industry_filter.split(',')
                industries.pop()

            ctc_filter = ''
            for salary in  salaries:
                ctc_filter += f'&ctcFilter={salary}'
            
            city_filter = ''
            for city in  _cities:
                city_filter += f'&cityTypeGid={city}'

            industry_filter = ''
            for industry in  industries:
                industry_filter += f'&industryTypeIdGid={industry}'

            
            logging.warning("{0} Program start time...".format(time.time()))
            scrap_naukri = ScrapNaukriJobs(language=language,ctc_string=ctc_filter,city_string=city_filter,industry_string=industry_filter)
            scrap_naukri.scrap_details()
            logging.warning("{0} Execution completed...".format(time.time()))
        return jsonify(cust_response(success = True,message="",status_code=200))


    except Exception as e:
        print(str(e))
        return jsonify(cust_response(success = False,message="Internal Server Error",status_code=500,data=[str(e)]))


@app.route('/scrap-linkdin-profiles',methods=['POST'])
def scrap_linkdin_profiles():
    try:
        if request.method == "POST":
            company_name = request.form.get('company_name')
            post_filter = request.form.get('post_filter')
            

            if not company_name:
                return jsonify(cust_response(success = False,message="Company required.",status_code=400))
        
            if not post_filter:
                return jsonify(cust_response(success = False,message="Designations required.",status_code=400))    

            if post_filter.endswith(','):
                posts = post_filter.split(',')
                posts.pop()       

            
            ScrapLinkdinJobs(company_name=[(constant.COMPANY_MAPPING[company_name],company_name)],post=posts).linkdin_login()

        return jsonify(cust_response(success = True,message="",status_code=200))
            
    except Exception as e:
        print(str(e),">>>>>>>>>>>>>>")
        print(traceback.format_exc())

        return jsonify(cust_response(success = False,message="Internal Server Error",status_code=500,data=[str(e)]))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/linkdin')
def linkdin_scrapping_filters():
    return render_template('linkdin_filter.html')

@app.route('/naukri')
def naukri_scrapping_filters():
    return render_template('naukri_filters.html')

@app.route('/linkdin-jobs')
def linkdin_job_scrapping_filters():
    return render_template('linkdin_job_filter.html')



@app.context_processor
def utility_processor():
    return {
        'salaries':constant.NAUKRI_SALARY,
        'cities':constant.NAUKRI_CITIES,
        'industry_types':constant.NAUKRI_INDUSTRY_TYPE,
        'designations':constant.DESIGNATIONS,
        'companies':constant.COMPANIES,
        "locations":constant.LOCATIONS
    }

if __name__ == '__main__':
    app.run(debug=True)