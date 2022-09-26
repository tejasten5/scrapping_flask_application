
function ajax_call(data,url){
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function (response) {
            console.log(response)
        },
        error: function (err) {
            
            if (err.status_code == 500){
                toastr["error"]("Internal server error .")
            }

        }
    })

}


function alert_validation(class_name,input_type,data_attribut,error_msg){
    let filter_string = ''
    let is_validated = true

    $(`.${class_name}`).each(function (idx, val) {
        if ($(val).is(':checked')) {
            filter_string += $(val).data(data_attribut) + ','
        }
    });

    if (filter_string.length == 0){
        toastr["error"](error_msg)

        
        toastr.options = {
            "closeButton": true,
            "progressBar": true,
            "positionClass": "toast-top-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
          }

          is_validated = false
         


    }    

    return {'filter_string':filter_string,'is_validated':is_validated}
}   


$(document).on('click', '#btn_naukri_scrapping', function () {
    


    let language = $('#formGroupExampleInput').val().trim()


    if (!language) {
        error_msg = "Please,Enter programming language."
        toastr["error"](error_msg)     

        return;

    }

    
    //  Salary filters 
    salary_result = alert_validation("salary_filters","checkbox","salvalue","Please,Select salary from given options.")
    if (! salary_result.is_validated)
        return ;
    
    //  City filter
    city_result = alert_validation("citi_filters","checkbox","city","Please,Select city from given options.")
    if (! city_result.is_validated)
        return ;

    // Industry filter
    industry_result = alert_validation("industry_filter","checkbox","industry","Please,Select industry from given options.")
    if (! industry_result.is_validated)
        return ;


    //  request payload data.
    data = {'language': language,'salary_filter': salary_result.filter_string,'city_filter': city_result.filter_string,'industry_filter':industry_result.filter_string}

    ajax_call(data,'/scrap-naukri')

})



$(document).on('click','#btn_linkdin_scrapping',function(){

    //  Salary 
    posts_filter = alert_validation("posts_filters","checkbox","postvalue","Please,Select designation from given options.")
    
    if (! posts_filter.is_validated)
        return ;
    

    // company_filters
    let company_name = $('.company_filters').data('comvalue')

    data = {
        'post_filter':post_filter,
        'company_name':company_name
    }

    url = '/scrap-linkdin-profiles'
    ajax_call(data,url)

})

