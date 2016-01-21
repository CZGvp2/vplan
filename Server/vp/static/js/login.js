$(document).ready(function () {
	$('#password').on('keyup keypress paste', function (event) {
		if (event.keyCode == 13 && !$('#password').val()) {
			event.preventDefault(); // Abfangen falls leer
			return false;
		}
		if ($('#password').val() || event.charCode) {
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
		})
	.on('focusout focus', function () {
		$(this).toggleClass('nofocus');
	});
	$('form').submit(function () {
		$('#hash').val( CryptoJS.SHA512($('#password').val()) );
		$('#password').val('');
	}
}
})