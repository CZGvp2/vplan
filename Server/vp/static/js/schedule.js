// Die is schön
filter = function(target) {
	var events = $('.event');
	if(target){
		for(var i=0; i < events.length; i++){
			var e = $(events[i]);
			var targets = e.data().targets.split(' ');

			if (targets.indexOf(target) < 0) e.hide();
			else e.show();
		}
	} else events.show();
}

removeFilter = function(){
  var events = $('.event');
  for(var i = 0; i < events.length; i++){
    $(events[i]).show();
  }
}

var currentIndex = 0;

prepSlides = function(){
  var slides = $('.slide');
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentIndex?'block':'none';
  $('#left').get(0).innerHTML = currentIndex>0?slides[currentIndex-1].children[0].innerHTML:'---';
  $('#right').get(0).innerHTML = currentIndex<slides.length-1?slides[currentIndex+1].children[0].innerHTML:'---';
}

max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }

var animationTime = 0.5;
var t_out = -1;

toggleSlide = function(dir){
  var slides = $(".slide");
  if(slides.length <= 1 || t_out >= 0) return;
  scrollTo(0,0)
  var nextSlide = dir=="left"?max(currentIndex-1, 0):min(currentIndex+1,slides.length-1);
  if(nextSlide!=currentIndex){
    for(var i = 0; i < slides.length; i++) slides[i].style.display = "none";
    slides[nextSlide].style.display = slides[currentIndex].style.display = "block";
    slides[currentIndex].style.animation = (nextSlide>currentIndex?"fade_left":"fade_right") + " " + animationTime + "s ease-in-out 0s 1";
    slides[nextSlide].style.animation = (nextSlide<currentIndex?"from_left":"from_right") + " " + animationTime + "s ease-in-out 0s 1";
    var tmpNext = nextSlide;
    var tmpCurr = currentIndex;
    slides[tmpNext].style.display = "block";
    t_out = window.setTimeout(function(){
        slides[tmpCurr].style.display = "none";
        t_out = -1;
    }, animationTime*1000);
  } else {
    slides[currentIndex].style.display = "none";
    slides[nextSlide].style.display = "block";
  }
  currentIndex = nextSlide;
  $("#left").get(0).innerHTML = currentIndex>0?slides[currentIndex-1].children[0].innerHTML:"---";
  $("#right").get(0).innerHTML = currentIndex<slides.length-1?slides[currentIndex+1].children[0].innerHTML:"---";
}

// EINE KOSTPROBE JQUERY
//... die nicht funktioniert?!? schau mal auf die Tagesnamen an den Seiten,
// wenn man toggleSlide in der .pt mit toggleSlide2 ersetzt hängt das updaten immer ne slide hinterher
/*toggleSlide2 = function(dir){
  var slides = $('.slide');
  if(slides.length <= 1) return;
  var nextIndex = dir=='left'?max(currentIndex-1, 0):min(currentIndex+1,slides.length-1);

  var currentSlide = $( slides[currentIndex] );
  var nextSlide = $( slides[nextIndex] );

  if(nextIndex != currentIndex){
    slides.hide();
    currentSlide.show();
    nextSlide.show();

    currentSlide.css({animation: (nextIndex>currentIndex?'fade_left':'fade_right') + ' ' + animationTime + 's ease-in-out 0s 1'});
    nextSlide.css({animation: (nextIndex<currentIndex?'from_left':'from_right') + ' ' + animationTime + 's ease-in-out 0s 1'});
    var tmpNext = $( slides[nextIndex] );
    var tmpCurr = $( slides[currentIndex] );
    window.setTimeout(function() {
        tmpNext.show();
        tmpCurr.hide();
    }, animationTime*1000);
  } else {
    currentSlide.hide();
    nextSlide.show();
  }
  currentIndex = nextIndex;
  var prev = currentSlide.prev('.slide');
  var next = currentSlide.next('.slide');
  $("#left").text(prev.length ? prev.find('div.slide_title').text() : '---');
  $("#right").text(next.length ? next.find('div.slide_title').text() : '---');
}*/

// Bist du jetzt glücklich?
// Add keylistener to toggle slides via arrow keys
$(document).on('keypress', function(evt){
  evt.preventDefault();
  evt.stopPropagation();
  switch(evt.keyCode){
    case 37: toggleSlide('left'); break;
    case 39: toggleSlide('right'); break;
  }
});

// Call prepSlides() when DOM is ready
$(prepSlides);
