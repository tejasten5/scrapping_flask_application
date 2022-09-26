from app import app as flask_app
from utils import constant,cust_response

@flask_app.context_processor
def utility_processor():
    return {
        'salaries':constant.NAUKRI_SALARY,
        'cities':constant.NAUKRI_CITIES,
        'industry_types':constant.NAUKRI_INDUSTRY_TYPE
    }
