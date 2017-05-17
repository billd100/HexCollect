$(document).ready(function() {
	var $dose_fields = $('#dose_fields');
		$dose_fields.toggleClass('hidden');
		
	var $dose_button = $('#dose_button');
		$dose_button.toggleClass('hidden');

	$dose_button.click(function() {
		var $dose_button_span = $('#dose_button_span');
		$dose_fields.slideToggle(75);
		$dose_fields.toggleClass('hidden');
		if ($dose_button_span.hasClass('glyphicon-plus')) {
			$dose_button_span.removeClass('glyphicon-plus');
			$dose_button_span.addClass('glyphicon-minus');
		} else {
			$dose_button_span.removeClass('glyphicon-minus');
			$dose_button_span.addClass('glyphicon-plus');
		}
	});


	// hide can_DELETE checkbox for JS users
	$(':checkbox').toggleClass('hidden');

	// check if field has text, if so, display
	function updateElementIndex(el, prefix, ndx) {
		var id_regex = new RegExp('(' + prefix + '-\\d+-)');
		var replacement = prefix + '-' + ndx + '-';
		if (el.id) {el.id = el.id.replace(id_regex, replacement)};
		if (el.name) {el.name = el.name.replace(id_regex, replacement)};
	}

	function addForm(btn, prefix){

		var formCount = parseInt($('#id_form-TOTAL_FORMS').val());
		
		// when single symptom is deleted
		var first_symptom = $('.symptom:first');
		if (formCount === 0 && first_symptom.hasClass('hidden')) {
			first_symptom.toggleClass('hidden');
			$('#id_form-TOTAL_FORMS').val(1);
		}
		else if (formCount < 10) {

			var $symptom = $('.symptom:last')
			$symptom.clone(true).insertAfter('.symptom:last').slideDown(300);

			// redeclare to get true last form
			var $symptom = $('.symptom:last')
			$symptom.css({'overflow': 'visible'});

			$symptom.children().each(function(){
				updateElementIndex(this, prefix, formCount);
			});
			$symptom.children().children().each(function(){
				updateElementIndex(this, prefix, formCount);
			});
			$symptom.children().children().children().each(function(){
				updateElementIndex(this, prefix, formCount);
			});

			$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
		}

	};

	function deleteForm(btn, prefix, id) {
		var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
		if (formCount === 1) {
			$('.symptom:first').toggleClass('hidden');
			$('#id_form-TOTAL_FORMS').val(0);
		} else {
			// if 'edit' in URL check delete instead of removing to remove symptom
			if (/edit/.test(window.location.href)) {
				$(btn).siblings(':checkbox').prop('checked', true);
				$(btn).parent('.symptom').toggleClass('hidden');
			} else {
				$(btn).parent('.symptom').remove();
			}
			var forms = $('.symptom');
			$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

			var i, max;
			for (i = 0, max = forms.length; i < max; i += 1){
				$(forms.get(i)).children().each(function(){
				updateElementIndex(this, prefix, i);
				});
				$(forms.get(i)).children().children().each(function(){
					updateElementIndex(this, prefix, i);
				});
				$(forms.get(i)).children().children().children().each(function(){
					updateElementIndex(this, prefix, i);
				});
			}
		}
	};

	$(".add_symptom").click(function(){
		return addForm(this, 'form');
	});
	$(".delete_symptom").click(function(){
		return deleteForm(this, 'form');
	});
	
});