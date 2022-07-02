function update_filter() {
    let min_area = GetUrlParameter("minarea");
    if (min_area!="") {
        $('#min-area').val(min_area);
    }
    let max_area = GetUrlParameter("maxarea");
    if (max_area!="") {
        $('#max-area').val(max_area);
    }
    let min_price = GetUrlParameter("minprice");
    if (min_price!="") {
        $('#min-price').val(min_price);
    }
    let max_price = GetUrlParameter("maxprice");
    if (max_price!="") {
        $('#max-price').val(max_price);
    }
    let sort = GetUrlParameter("sort");
    if (sort!="") {
        $('#sort-mode').val(sort);
    }
    let type = GetUrlParameter("type");
    if (type!="") {
        $("#type-select").val(type);
    }
}

function render_address_item_option(item, selected_item=-1) {
    if (item[0]!=selected_item) {
        return `<option value="${item[0]}">${item[1]}</option>`
    } else {
        return `<option value="${item[0]}" selected>${item[1]}</option>`
    }
}

function render_list_districts(data) {
    if (data["status"]==true) {
        let district = GetUrlParameter("district");
        let district_code = -1;
        if (district != "") {
            district_code = parseInt(district);
        }
        let district_size = data["data"].length;
        let append_content = "";
        for (let i=0; i<district_size; i++) {
            let item = data["data"][i];
            let child = render_address_item_option(item, district_code);
            append_content = append_content+child;
        }
        let old_content = $('#district-select').html()
        let content = old_content + append_content
        $('#district-select').html(content);
        if (district_code != -1) {
            fetch_wards_data(district=district_code, callback_func=render_list_wards_and_update)
        }
    }
}

function render_list_wards(data) {
    if (data["status"]==true) {
        let district_size = data["data"].length;
        let append_content = "";
        for (let i=0; i<district_size; i++) {
            let item = data["data"][i];
            let child = render_address_item_option(item);
            append_content = append_content+child;
        }
        let old_content = $('#ward-select').html()
        let content = old_content + append_content
        $('#ward-select').html(content);
    }
}

function render_list_wards_and_update(data) {
    if (data["status"]==true) {
        let district = GetUrlParameter("ward");
        let district_code = -1;
        if (district != "") {
            district_code = parseInt(district);
        }
        let district_size = data["data"].length;
        let append_content = "";
        for (let i=0; i<district_size; i++) {
            let item = data["data"][i];
            let child = render_address_item_option(item, district_code);
            append_content = append_content+child;
        }
        let old_content = $('#ward-select').html()
        let content = old_content + append_content
        $('#ward-select').html(content);
    }
}

function GetUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1);
    let sURLVariables = sPageURL.split('&');
    for (let i = 0; i < sURLVariables.length; i++) {
        let sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
    return "";
}

$('#district-select').on('change', function (event) {
    let value = $(this).val();
    $('#ward-select').children().remove();
    $('#ward-select').append(`<option value="-1" selected>Phường/xã</option>`);
    if (value == -1) {
        $('#ward-select').prop('disabled',true);
    } else {
        $('#ward-select').prop('disabled',false);
        fetch_wards_data(district=value, callback_func=render_list_wards)
    }
});

$("#min-area").on('keyup', function(event) {
    let value = $(this).val();
    value = number_str_format(value);
    $(this).val(value);
});

$("#max-area").on('keyup', function(event) {
    let value = $(this).val();
    value = number_str_format(value);
    $(this).val(value);
});

$("#min-price").on('keyup', function(event) {
    let value = $(this).val();
    value = number_str_format(value);
    $(this).val(value);
});
$("#max-price").on('keyup', function(event) {
    let value = $(this).val();
    value = number_str_format(value);
    $(this).val(value);
});