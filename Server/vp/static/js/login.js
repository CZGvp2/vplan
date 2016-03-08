// Make submit of the first form of the page available globally
function submit() {
	$('form').submit();
}

// Update keylisteners
$(function () {
	$("#jsWarn").hide();
	$('#password').on('keyup keypress paste', function (event) {
		if (event.keyCode == 13 && $('#password').val())
			submit();

		if ($('#password').val() || event.charCode) {
			$('a#submit').css({'background-color':'#316495', 'cursor':'pointer'})
			.off('click').on('click', submit);
			$('#password').css('border-bottom-color', '#316495');
			$('div#submit').css('margin-top', '73px');
			$('#incorrect').hide();
		}
		else {
			$('a#submit').css({'background-color':'#232323', 'cursor':'default'})
			.off('click');
		}
	})
	.on('focusout focus', function () {
		$(this).toggleClass('nofocus');
	});
	$('form').submit(function () {
		$('#hash').val( CryptoJS.SHA512($('#password').val() ) ); // TODO random strings hinzufügen
		$('#password').val('');
	});
});

// Check if jQuery is loading correctly
(jQCheck = function(){
	if(typeof $ == 'undefined') alert('(ERROR) jQuery konnte nicht geladen werden. Bitte wende dich an einen Server-Admin.')
})();
