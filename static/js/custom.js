// // let autocomplete;



// function initAutoComplete(){
//     var quezon_city = new google.maps.LatLngBounds(
//         new google.maps.LatLng(14.777775, 121.134932),
//         new google.maps.LatLng(14.605136, 120.988440));
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_information-address'),
//     {
//         types: ['geocode', 'establishment'],
//         // //default in this app is "IN" - add your country code
//         componentRestrictions: {'country': ['ph']},
//         // bounds: quezon_city,
//     // strictBounds: true,
//     })
// // function to specify what should happen when the prediction is clicked
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged (){
    
//     var place = autocomplete.getPlace();
    
//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_information-address').placeholder = "Start typing...";
//     }
//     else{
//         // console.log('place name=>', place.name)
//     }

//     // get the address components and assign them to the fields
//     // console.log(place);
//     var geocoder = new google.maps.Geocoder()
//     var address = document.getElementById('id_information-address').value

//     geocoder.geocode({'address': address}, function(results, status){
//         // console.log('results=>', results)
//         // console.log('status=>', status)
//         if(status == google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             // console.log('lat=>', latitude);
//             // console.log('long=>', longitude);
//             $('#id_information-latitude').val(latitude);
//             $('#id_information-longitude').val(longitude);

//             $('#id_information-address').val(address);
//         }
//     });

//     // loop through the address components and assign other address data
//     console.log(place.address_components);
//     for(var i=0; i<place.address_components.length; i++){
//         for(var j=0; j<place.address_components[i].types.length; j++){
//             // get country
//             if(place.address_components[i].types[j] == 'country'){
//                 $('#id_information-country').val(place.address_components[i].long_name);
//             }
//             // get state
//             if(place.address_components[i].types[j] == 'administrative_area_level_1'){
//                 $('#id_information-state').val(place.address_components[i].long_name);
//             }
//             // get city
//             if(place.address_components[i].types[j] == 'locality'){
//                 $('#id_information-city').val(place.address_components[i].long_name);
//             }
//             // get pincode
//             if(place.address_components[i].types[j] == 'postal_code'){
//                 $('#id_information-pin_code').val(place.address_components[i].long_name);
//             }else{
//                 $('#id_information-pin_code').val("");
//             }
//         }
//     }

// }

var input = document.getElementById('id_information-address');
var options = {
    componentRestrictions: {
        country: 'ph'
    }
};

var autocomplete = new google.maps.places.Autocomplete(input, options);

$(input).on('input',function(){
	var str = input.value;
  var prefix = 'Quezon City, ';
	if(str.indexOf(prefix) == 0) {
		console.log(input.value);
	} else {
		if (prefix.indexOf(str) >= 0) {
    	input.value = prefix;
    } else {
  		input.value = prefix+str;
   }
	}

});

google.maps.event.addListener(autocomplete, 'place_changed', function () {
    
    var place = autocomplete.getPlace();
    
    // User did not select the prediction. Reset the input field or alert()
    

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_information-address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_information-latitude').val(latitude);
            $('#id_information-longitude').val(longitude);

            $('#id_information-address').val(address);
        }
    })

    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_information-country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_information-state').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] == 'sublocality'){
                $('#inputbarangay').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_information-city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_information-pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_information-pin_code').val("");
            }
        }
    }
    
});




$("#id_general-accident_factor").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const accidentId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'accident_factor_id': accidentId       // add the country id to the GET parameters
        },
        success: function (data) {
            let select_element = $('#id_general-accident_subcategory'); //Sub_category select  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $(select_element).html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '';
            data.forEach(function (accident_subcategory) {
                html_data += `<option value="${accident_subcategory.id}">${accident_subcategory.sub_category}</option>`
            });
            console.log(html_data);
            $("#id_general-accident_subcategory").html(html_data);

        }
    });

});



$("#id_general-collision_type").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const collisionId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'collision_type_id': collisionId       // add the country id to the GET parameters
        },
        success: function (data) {  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $("#id_general-collision_subcategory").html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '<option value="">---------</option>';
            data.forEach(function (collision_subcategory) {
                html_data += `<option value="${collision_subcategory.id}">${collision_subcategory.sub_category}</option>`
                
            });
            console.log(html_data);
            // $("#id_general-collision_subcategory").html(html_data);
            // if ($("#id_general-collision_subcategory").find(html_data).length <= 1){
            //     $("#id_general-collision_subcategory").disable=true;
            // }

        }
    });

});

$("#id_accident_factor").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const accidentId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'accident_factor_id': accidentId       // add the country id to the GET parameters
        },
        success: function (data) {
            let select_element = $('#id_accident_subcategory'); //Sub_category select  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $(select_element).html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '';
            data.forEach(function (accident_subcategory) {
                html_data += `<option value="${accident_subcategory.id}">${accident_subcategory.sub_category}</option>`
            });
            console.log(html_data);
            $("#id_accident_subcategory").html(html_data);

        }
    });
    console.log(data);
});

$("#id_collision_type").change(function () {
    const url = $("#form_incidentgeneral").attr("data-acc-url");  // get the url of the `load_cities` view
    const collisionId = $(this).val();  // get the selected country ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'collision_type_id': collisionId       // add the country id to the GET parameters
        },
        success: function (data) {  
            //console.log(data) // `data` is the return of the `load_cities` view function
            $("#id_collision_subcategory").html(data);  // replace the contents of the city input with the data that came from the server

            let html_data = '<option value="">---------</option>';
            data.forEach(function (collision_subcategory) {
                html_data += `<option value="${collision_subcategory.id}">${collision_subcategory.sub_category}</option>`
                
            });
            console.log(html_data);
            // $("#id_general-collision_subcategory").html(html_data);
            // if ($("#id_general-collision_subcategory").find(html_data).length <= 1){
            //     $("#id_general-collision_subcategory").disable=true;
            // }

        }
    });

});

//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches


$(".next").click(function(){
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent();
    next_fs = $(this).parent().next();

    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            scale = 1 - (1 - now) * 0.2;
            //2. bring next_fs from the right(50%)
            left = (now * 50)+"%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
            next_fs.css({'left': left, 'opacity': opacity});
        },
        duration: 800,
        complete: function(){
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

$(".previous").click(function(){
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1-now) * 50)+"%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
        },
        duration: 800,
        complete: function(){
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

document.getElementById("add_people").onclick=function (ev) {
    
            var image=document.getElementById("people");
            
            var div = document.createElement('div');
            div.className = 'form-row';

            var div_1 = document.createElement('div');
            div_1.className = 'form-group col-md-4';

            var div_2 = document.createElement('div');
            div_2.className = 'form-group col-md-4';

            var div_3 = document.createElement('div');
            div_3.className = 'form-group col-md-4';

            var label_firstname = document.createElement('label');
            label_firstname.textContent = 'First Name'

            var input_firstname = document.createElement('input');
            input_firstname.className = 'form-control';
            input_firstname.type="text";
            input_firstname.id = 'first_name'

            var label_middlename = document.createElement('label');
            label_middlename.textContent = 'Middle Name'

            var input_middlename = document.createElement('input');
            input_middlename.className = 'form-control';
            input_middlename.type="text";

            var label_lastname = document.createElement('label');
            label_lastname.textContent = 'Last Name'

            var input_lastname = document.createElement('input');
            input_lastname.className = 'form-control';
            input_lastname.type="text";

            var div_a = document.createElement('div');
            div_a.className = 'form-row';

            var div_4 = document.createElement('div');
            div_4.className = 'form-group col-md-6';

            var div_5 = document.createElement('div');
            div_5.className = 'form-group col-md-6';

            var div_6 = document.createElement('div');
            div_6.className = 'form-group col-md-12';


            var label_age = document.createElement('label');
            label_age.textContent = 'Age'

            var input_age = document.createElement('input');
            input_age.className = 'form-control';
            input_age.type="text";

            var label_gender = document.createElement('label');
            label_gender.textContent = 'Gender'

            var input_gender = document.createElement('input');
            input_gender.className = 'form-control';
            input_gender.type="text";

            var label_address = document.createElement('label');
            label_address.textContent = 'Address'

            var input_address = document.createElement('input');
            input_address.className = 'form-control';
            input_address.type="text";

            var newInput=document.createElement("input");
            newInput.type="file";
            newInput.name="file[]";

            var div_b = document.createElement('div');
            div_b.className = 'form-row';

            var div_7 = document.createElement('div');
            div_7.className = 'form-group col-md-4';

            var div_8 = document.createElement('div');
            div_8.className = 'form-group col-md-4';

            var div_9 = document.createElement('div');
            div_9.className = 'form-group col-md-4';

            var label_involvement = document.createElement('label');
            label_involvement.textContent = 'Involvement'

            var select_involvement = document.createElement('select');
            select_involvement.className = 'form-control';

            var label_id = document.createElement('label');
            label_id.textContent = 'ID Presented'

            var select_id = document.createElement('select');
            select_id.className = 'form-control';

            var label_idnumber = document.createElement('label');
            label_idnumber.textContent = 'ID Number'

            var input_idnumber = document.createElement('input');
            input_idnumber.className = 'form-control';
            input_idnumber.type="text";

            
            var div_10 = document.createElement('div');
            div_10.className = 'form-group';

            var label_injury = document.createElement('label');
            label_injury.textContent = 'Injury'

            var select_injury = document.createElement('select');
            select_injury.className = 'form-control';

            var div_11 = document.createElement('div');
            div_11.className = 'form-group';

            var label_drivererror = document.createElement('label');
            label_drivererror.textContent = 'Driver Error'

            var select_drivererror = document.createElement('select');
            select_drivererror.className = 'form-control';

            var option_a = new Option("---------",);
            var option = new Option("Pedestrian",);
            var option1 = new Option("Witness");
            var option2 = new Option("Passenger");
            var option3 = new Option("Driver");

            var option_b = new Option("---------",);
            var option4 = new Option("Driver's License",);
            var option5 = new Option("Government ID");
            var option6 = new Option("Passsport");
            var option7 = new Option("School ID");

            var option_c = new Option("---------",);
            var option8 = new Option("Fatal",);
            var option9 = new Option("Minor");
            var option10 = new Option("Not Injured");
            var option11 = new Option("Serious");

            var option_d = new Option("---------",);
            var option12 = new Option("Bad Overtaking",);
            var option13 = new Option("Bad Turning");
            var option14 = new Option("Fatigued / Asleep");
            var option15 = new Option("Inattentive");
            var option16 = new Option("No Signal");
            var option17 = new Option("Too Close");
            var option18 = new Option("Too Fast");
            var option19 = new Option("Using Cellphone");

            var option_e = new Option("---------",);
            var option20 = new Option("Alcohol suspected",);
            var option21 = new Option("Drugs suspected");

            var option_f = new Option("---------",);
            var option22 = new Option("Seat belt/Helmet Worn",);
            var option23 = new Option("Not worn");
            var option24 = new Option("Not worn correctly");

            var div_12 = document.createElement('div');
            div_12.className = 'form-group';

            var label_alcoholdrugs = document.createElement('label');
            label_alcoholdrugs.textContent = 'Alcohol / Drugs'

            var select_alcoholdrugs = document.createElement('select');
            select_alcoholdrugs.className = 'form-control';

            var div_13 = document.createElement('div');
            div_13.className = 'form-group';

            var label_seatbelt = document.createElement('label');
            label_seatbelt.textContent = 'Seat belt / Helmet'

            var select_seatbelt = document.createElement('select');
            select_seatbelt.className = 'form-control';
    
    
            var br=document.createElement("br");
            var br1=document.createElement("br");
    
            image.appendChild(div);
            div.appendChild(div_1);
            div_1.appendChild(label_firstname);
            div_1.appendChild(input_firstname);
            image.appendChild(div);
            div.appendChild(div_2);
            div_2.appendChild(label_middlename);
            div_2.appendChild(input_middlename);
            image.appendChild(div);
            div.appendChild(div_3);
            div_3.appendChild(label_lastname);
            div_3.appendChild(input_lastname);

            image.appendChild(div_a);

            div_a.appendChild(div_4);
            div_4.appendChild(label_age);
            div_4.appendChild(input_age);

            div_a.appendChild(div_5);
            div_5.appendChild(label_gender);
            div_5.appendChild(input_gender);

            image.appendChild(div_6);
            div_6.appendChild(label_address);
            div_6.appendChild(input_address);

            image.appendChild(div_b);

            div_b.appendChild(div_7);
            div_7.appendChild(label_involvement);
            div_7.appendChild(select_involvement);
            select_involvement.appendChild(option_a);
            select_involvement.appendChild(option);
            select_involvement.appendChild(option1);
            select_involvement.appendChild(option2);
            select_involvement.appendChild(option3);

            div_b.appendChild(div_8);
            div_8.appendChild(label_id);
            div_8.appendChild(select_id);
            select_id.appendChild(option_b);
            select_id.appendChild(option4);
            select_id.appendChild(option5);
            select_id.appendChild(option6);
            select_id.appendChild(option7);

            div_b.appendChild(div_9);
            div_9.appendChild(label_idnumber);
            div_9.appendChild(input_idnumber);

            image.appendChild(div_10);
            div_10.appendChild(label_injury);
            div_10.appendChild(select_injury);
            select_injury.appendChild(option_c);
            select_injury.appendChild(option8);
            select_injury.appendChild(option9);
            select_injury.appendChild(option10);
            select_injury.appendChild(option11);

            image.appendChild(div_11);
            div_11.appendChild(label_drivererror);
            div_11.appendChild(select_drivererror);
            select_drivererror.appendChild(option_d);
            select_drivererror.appendChild(option12);
            select_drivererror.appendChild(option13);
            select_drivererror.appendChild(option14);
            select_drivererror.appendChild(option15);
            select_drivererror.appendChild(option16);
            select_drivererror.appendChild(option17);
            select_drivererror.appendChild(option18);
            select_drivererror.appendChild(option19);

            image.appendChild(div_12);
            div_12.appendChild(label_alcoholdrugs);
            div_12.appendChild(select_alcoholdrugs);
            select_alcoholdrugs.appendChild(option_e);
            select_alcoholdrugs.appendChild(option20);
            select_alcoholdrugs.appendChild(option21);

            image.appendChild(div_13);
            div_13.appendChild(label_seatbelt);
            div_13.appendChild(select_seatbelt);
            select_seatbelt.appendChild(option_f);
            select_seatbelt.appendChild(option22);
            select_seatbelt.appendChild(option23);
            select_seatbelt.appendChild(option24);

        }

        document.getElementById("add_vehicle").onclick=function (ev) {
    
            var image=document.getElementById("vehicle");
            
            var div = document.createElement('div');
            div.className = 'form-row';

            var div_1 = document.createElement('div');
            div_1.className = 'form-group col-md-4';

            var div_2 = document.createElement('div');
            div_2.className = 'form-group col-md-4';

            var div_3 = document.createElement('div');
            div_3.className = 'form-group col-md-4';

            var label_classification = document.createElement('label');
            label_classification.textContent = 'Classification'

            var select_classification = document.createElement('select');
            select_classification.className = 'form-control';

            var label_vehicle = document.createElement('label');
            label_vehicle.textContent = 'Vehicle Type'

            var select_vehicle = document.createElement('select');
            select_vehicle.className = 'form-control';


            var label_brand = document.createElement('label');
            label_brand.textContent = 'Make / Brand'

            var input_brand = document.createElement('input');
            input_brand.className = 'form-control';
            input_brand.type="text";
            

            var label_platenumber = document.createElement('label');
            label_platenumber.textContent = 'Plate Number'

            var input_platenumber = document.createElement('input');
            input_platenumber.className = 'form-control';
            input_platenumber.type="text";

            var label_enginenumber = document.createElement('label');
            label_enginenumber.textContent = 'Engine Number'

            var input_enginenumber = document.createElement('input');
            input_enginenumber.className = 'form-control';
            input_enginenumber.type="text";

            var label_chassisnumber = document.createElement('label');
            label_chassisnumber.textContent = 'Chassis Number'

            var input_chassisnumber = document.createElement('input');
            input_chassisnumber.className = 'form-control';
            input_chassisnumber.type="text";

            var label_insurance = document.createElement('label');
            label_insurance.textContent = 'Insurance Details'

            var input_insurance = document.createElement('input');
            input_insurance.className = 'form-control';
            input_insurance.type="text";



            var div_a = document.createElement('div');
            div_a.className = 'form-row';

            var div_4 = document.createElement('div');
            div_4.className = 'form-group col-md-4';

            var div_5 = document.createElement('div');
            div_5.className = 'form-group col-md-4';

            var div_6 = document.createElement('div');
            div_6.className = 'form-group col-md-4';

            var div_b = document.createElement('div');
            div_b.className = 'form-row';

            var div_7 = document.createElement('div');
            div_7.className = 'form-group';

            var div_8 = document.createElement('div');
            div_8.className = 'form-group';

            var div_9 = document.createElement('div');
            div_9.className = 'form-group';

            var div_10 = document.createElement('div');
            div_10.className = 'form-group';

            var div_11 = document.createElement('div');
            div_11.className = 'form-group';

            var div_12 = document.createElement('div');
            div_12.className = 'form-group';

            var label_manuever = document.createElement('label');
            label_manuever.textContent = 'Maneuver'

            var select_manuever = document.createElement('select');
            select_manuever.className = 'form-control';

            var label_damage = document.createElement('label');
            label_damage.textContent = 'Damage'

            var select_damage = document.createElement('select');
            select_damage.className = 'form-control';

            var label_defect= document.createElement('label');
            label_defect.textContent = 'Defect'

            var select_defect = document.createElement('select');
            select_defect.className = 'form-control';

            var label_loading= document.createElement('label');
            label_loading.textContent = 'Loading'

            var select_loading = document.createElement('select');
            select_loading.className = 'form-control';



            var option_a = new Option("---------",);
            var option = new Option("Diplomat",);
            var option1 = new Option("Government");
            var option2 = new Option("Private");
            var option3 = new Option("Public / For Hire");

            var option_b = new Option("---------",);
            var option4 = new Option("Ambulance",);
            var option5 = new Option("Animal");
            var option6 = new Option("Armored Car");
            var option7 = new Option("Bicycle");
            var option8 = new Option("Bus",);
            var option9 = new Option("Car");
            var option10 = new Option("Electric Bike");
            var option11 = new Option("Habal-habal");
            var option12 = new Option("Heavy Equipment",);
            var option13 = new Option("Horse-Driven Carriage (Tartanilla)");
            var option14 = new Option("Jeepney");
            var option15 = new Option("Motorcycle");
            var option16 = new Option("Pedestrian");
            var option17 = new Option("Pedicab");
            var option18 = new Option("Push-Cart");
            var option19 = new Option("SUV");
            var option10 = new Option("Taxi (metered)");
            var option11 = new Option("Tricycle");
            var option12 = new Option("Truck (Articulated)",);
            var option13 = new Option("Truck (Fire)");
            var option14 = new Option("Truck (Pick-up)");
            var option15 = new Option("Truck (Rigid)");
            var option16 = new Option("Truck (Unknown)");
            var option17 = new Option("Van");
            var option18 = new Option("Water Vessel");
            var option19 = new Option("Others");

            var option_c = new Option("---------",);
            var option20 = new Option("Left-turn",);
            var option21 = new Option("Right-turn");
            var option22 = new Option("U-turn");
            var option23 = new Option("Cross Traffic");
            var option24 = new Option("Merging",);
            var option25 = new Option("Diverging");
            var option26 = new Option("Overtaking");
            var option27 = new Option("Going Ahead");
            var option28 = new Option("Reversing");
            var option29 = new Option("Sudden Start",);
            var option30 = new Option("Sudden Stop");
            var option31 = new Option("Parked Off Road");
            var option32 = new Option("Parked On Road");

            var option_d = new Option("---------",);
            var option33 = new Option("None",);
            var option34 = new Option("Front");
            var option35 = new Option("Left");
            var option36 = new Option("Multiple");
            var option37 = new Option("Rear",);
            var option38 = new Option("Right");
            var option39 = new Option("Roof");

            var option_e = new Option("---------",);
            var option40 = new Option("None",);
            var option41 = new Option("Breaks");
            var option42 = new Option("Lights");
            var option43 = new Option("Multiple");
            var option44 = new Option("Steering",);
            var option45 = new Option("Tires");

            var option_f = new Option("---------",);
            var option46 = new Option("Legal",);
            var option47 = new Option("Overloaded");
            var option48 = new Option("Unsafe Load");
            var option49 = new Option("Others");


            var div_12 = document.createElement('div');
            div_12.className = 'form-group';

            var label_alcoholdrugs = document.createElement('label');
            label_alcoholdrugs.textContent = 'Alcohol / Drugs'

            var select_alcoholdrugs = document.createElement('select');
            select_alcoholdrugs.className = 'form-control';

            var div_13 = document.createElement('div');
            div_13.className = 'form-group';

            var label_seatbelt = document.createElement('label');
            label_seatbelt.textContent = 'Alcohol / Drugs'

            var select_seatbelt = document.createElement('select');
            select_seatbelt.className = 'form-control';
    
    
            var br=document.createElement("br");
            var br1=document.createElement("br");
    
            image.appendChild(div);
            div.appendChild(div_1);
            div_1.appendChild(label_classification);
            div_1.appendChild(select_classification);
            select_classification.appendChild(option_a);
            select_classification.appendChild(option);
            select_classification.appendChild(option1);
            select_classification.appendChild(option2);
            select_classification.appendChild(option3);
            
            image.appendChild(div);
            div.appendChild(div_2);
            div_2.appendChild(label_vehicle);
            div_2.appendChild(select_vehicle);
            select_vehicle.appendChild(option_b);
            select_vehicle.appendChild(option4);
            select_vehicle.appendChild(option5);
            select_vehicle.appendChild(option6);
            select_vehicle.appendChild(option7);
            select_vehicle.appendChild(option8);
            select_vehicle.appendChild(option9);
            select_vehicle.appendChild(option10);
            select_vehicle.appendChild(option11);
            select_vehicle.appendChild(option12);
            select_vehicle.appendChild(option13);
            select_vehicle.appendChild(option14);
            select_vehicle.appendChild(option15);
            select_vehicle.appendChild(option16);
            select_vehicle.appendChild(option17);
            select_vehicle.appendChild(option18);
            select_vehicle.appendChild(option19);
            
            image.appendChild(div);
            div.appendChild(div_3);
            div_3.appendChild(label_brand);
            div_3.appendChild(input_brand);

            image.appendChild(div_a);

            div_a.appendChild(div_4);
            div_4.appendChild(label_platenumber);
            div_4.appendChild(input_platenumber);

            div_a.appendChild(div_5);
            div_5.appendChild(label_enginenumber);
            div_5.appendChild(input_enginenumber);

            div_a.appendChild(div_6);
            div_6.appendChild(label_chassisnumber);
            div_6.appendChild(input_chassisnumber);

            image.appendChild(div_7);
            div_7.appendChild(label_insurance);
            div_7.appendChild(input_insurance);

            image.appendChild(div_8);
            div_8.appendChild(label_manuever);
            div_8.appendChild(select_manuever);
            select_manuever.appendChild(option_c);
            select_manuever.appendChild(option20);
            select_manuever.appendChild(option21);
            select_manuever.appendChild(option22);
            select_manuever.appendChild(option23);
            select_manuever.appendChild(option24);
            select_manuever.appendChild(option25);
            select_manuever.appendChild(option26);
            select_manuever.appendChild(option27);
            select_manuever.appendChild(option28);
            select_manuever.appendChild(option29);
            select_manuever.appendChild(option30);
            select_manuever.appendChild(option31);
            select_manuever.appendChild(option32);



            image.appendChild(div_9);
            div_9.appendChild(label_damage);
            div_9.appendChild(select_damage);
            select_damage.appendChild(option_d);
            select_damage.appendChild(option33);
            select_damage.appendChild(option34);
            select_damage.appendChild(option35);
            select_damage.appendChild(option36);
            select_damage.appendChild(option37);
            select_damage.appendChild(option38);
            select_damage.appendChild(option39);

            image.appendChild(div_10);
            div_10.appendChild(label_defect);
            div_10.appendChild(select_defect);
            select_defect.appendChild(option_e);
            select_defect.appendChild(option40);
            select_defect.appendChild(option41);
            select_defect.appendChild(option42);
            select_defect.appendChild(option43);
            select_defect.appendChild(option44);
            select_defect.appendChild(option45);
        
            image.appendChild(div_11);
            div_11.appendChild(label_loading);
            div_11.appendChild(select_loading);
            select_loading.appendChild(option_f);
            select_loading.appendChild(option46);
            select_loading.appendChild(option47);
            select_loading.appendChild(option48);
            select_loading.appendChild(option49);

        }

        document.getElementById("add_image").onclick=function (ev) {
    
            var image=document.getElementById("images");
    
            
            var div_a = document.createElement('div');
            div_a.className = 'form-row';
            var div_b = document.createElement('div');
            div_b.className = 'form-row';
    
            var description=document.createElement("textarea");
            description.className = 'form-control';
            description.name="desc[]";

            var newInput=document.createElement("input");
            newInput.type="file";
            newInput.name="file[]";
    
    
            var br=document.createElement("br");
            var br1=document.createElement("br");
    
            
            
    
            image.appendChild(div_a);
            div_a.appendChild(description);
            image.appendChild(div_b);
            div_b.appendChild(newInput);
    
        }
