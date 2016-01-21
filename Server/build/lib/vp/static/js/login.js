function change(evt) {
	if (evt.keyCode == 13 && !$('#password').val()) {
		evt.preventDefault(); // Abfangen falls leer
		return false;
	}
	if ($('#password').val() || evt.charCode) {
		$('a#submit').css({'background-color':'#88A6FF', 'cursor':'pointer'})
		  .click(function () {
		  	$('form').submit();
		  });
		$('#password').css('border-bottom-color', '#88A6FF');
		$('div#submit').css('margin-top', '73px');
		$('#incorrect').hide();
	}
	else
		$('a#submit').css({'background-color':'#DCDCDC', 'cursor':'auto'})
		  .click(function () {});
}
$(document).ready(function () {
	$('#password').on('keyup keypress paste', change)
	  .on('focusout focus', function () {
		$(this).toggleClass('nofocus');
	})
})