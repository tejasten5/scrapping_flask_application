def cust_response(**params):
    success = params.get('success') or False
    message = params.get('message') or ''
    errors = params.get('errors') or []
    data = params.get('data') or ([] if params.get('data')==[] else {})
    status_code = params.get('status_code') or status.HTTP_200_OK

    response_data = {
        'success': success,
        'errors': errors,
        'data': data,
        'message': message
    }   

    return response_data