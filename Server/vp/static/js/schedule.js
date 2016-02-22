// as always, jQuery has the solution
function filter(target) {
	var events = $('.event');
	if (target) {
		for (var i=0; i < events.length; i++) {
			var e = $(events[i]);
			var targets = e.data().targets.split(' ');

			if (targets.indexOf(target) < 0) e.hide();
			else e.show();
		}
	} else events.show();
}