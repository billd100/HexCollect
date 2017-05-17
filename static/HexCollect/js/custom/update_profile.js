var condition_input = document.getElementById('update_profile_conditions');
var conditions_hidden = document.getElementById('conditions_hidden');

var condition_intervention_form = document.getElementById('condition_intervention_form');
// noscript displays form, need to remove hidden class from form for js
condition_intervention_form.className = "";

var condition_list = document.getElementById('condition_list');
var li = document.createElement('li');

var duplicate_condition = document.getElementById('duplicate_condition');

var duplicate_error = "Oops, you have already listed this condition.";

condition_input.addEventListener("keyup", addToHidden, false);

function addToHidden(e) {
	e = e || event; // true returns first, false returns second operand
	if (e.keyCode === 13) {
		// add user input to hidden input value with all conditions
		if (~conditions_hidden.value.indexOf(condition_input.value) && condition_input.value != "") {
			// duplicate_error is fixed and becomes sole content of duplicate_condition p element
			duplicate_condition.innerHTML = duplicate_error;
		}
		else if (condition_input.value === "") {
			return;	
		}
		else {
			// clear error message
			duplicate_condition.innerHTML = "";
			
			// add user input to hidden input
			conditions_hidden.value += condition_input.value;
			
			// clone new_li (false for no children to clone), createTextNode of user input (to escape HTML a user may have entered), append user input to li, append li to ul
			var new_li = li.cloneNode(false)
			var li_text = document.createTextNode(condition_input.value)
			new_li.appendChild(li_text);
			condition_list.appendChild(new_li);
			
			// clear user input box
			condition_input.value = "";

			// call ajax function
			add_condition();
			
			// clear hidden input
			conditions_hidden.value = "";
		}
	}
}


function add_condition() {
	
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	console.log('add_condition called');
	
	function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
	$.ajaxSetup({
		beforeSend : function(xhr,settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$.ajax({
		url : "/u/update_conditions/",
		type : "POST",
		data : { condition : $('#condition_hidden').val() },
		
		success : function(json) {
			$('#condition_hidden').val('');
			console.log(json);
			console.log('success');
		},
		
		error : function(xhr,errmsg,err) {
			$('#duplicate_condition').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
		}
	});
};



















