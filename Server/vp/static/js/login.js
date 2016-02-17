function submit() {
	$('form').submit();
}
$(document).ready(function () {
	$('#password').on('keyup keypress paste', function (event) {
		if (event.keyCode == 13 && $('#password').val())
			submit();

		if ($('#password').val() || event.charCode) {
			$('a#submit').css({'background-color':'#88A6FF', 'cursor':'pointer'})
			.off('click').on('click', submit);
			$('#password').css('border-bottom-color', '#88A6FF');
			$('div#submit').css('margin-top', '73px');
			$('#incorrect').hide();
		}
		else {
			$('a#submit').css({'background-color':'#DCDCDC', 'cursor':'default'})
			.off('click');
		}
	})
	.on('focusout focus', function () {
		$(this).toggleClass('nofocus');
	});
	$('form').submit(function () {
		$('#hash').val( CryptoJS.SHA512($('#password').val()) );
		$('#password').val('');
	});
}); // das Semikolon hat gefehlt
(jQCheck = function(){
	if(typeof $ === 'undefined') alert('(ERROR) jQuery konnte nicht geladen werden. Bitte wende dich an einen Server-Admin.')
})();