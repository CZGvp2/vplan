function filter(target) {
	var events = $('.event');
	if (target) {
		for (var i=0; i < events.length; i++) {
			var e = $(events[i]);
			var targets = e.data().targets.split(' ');

			if (targets.indexOf(target) < 0) e.hide();
			else e.show();
		}
	} else events.show(); // target = null -> alles angezeigt
}

var currentIndex = 0; // Irgendwie muss das dann am anfang der Index von der Slide von heute sein

// Alle Slides müssen ein vorgefertigtes Style-setup bekommen:
prepSlides = function(){
  var slides = $('.slide');
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentSlide?'block':'none';
  $('#left').get(0).innerHTML = currentSlide>0?slides[currentSlide-1].children[0].innerHTML:'---';
  $('#right').get(0).innerHTML = currentSlide<slides.length-1?slides[currentSlide+1].children[0].innerHTML:'---';
}

max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }
var animationTime = 0.5;
// 'harte' Übergänge: aus- und einblenden statt blenden nach links und rechts;
// funktioniert so aber immerhin
toggleSlide = function(dir){
  var slides = $(".slide");
  if(slides.length <= 1) return;
  var nextSlide = dir=="left"?max(currentSlide-1, 0):min(currentSlide+1,slides.length-1);
  console.log("[DEBUG] SlideEvent // old:" + currentSlide + " new:" + nextSlide);
  // hier könnte man mit css3 transitions u. animations nen schönen Übergang bauen
// currentSlide = aktuelle Folie, wird ausgebaut
// nextSlide wird eingebaut
  if(nextSlide!=currentSlide){
    for(var i = 0; i < slides.length; i++) slides[i].style.display = "none";
    slides[nextSlide].style.display = slides[currentSlide].style.display = "block";
    slides[currentSlide].style.animation = (nextSlide>currentSlide?"fade_left":"fade_right") + " " + animationTime + "s ease-in-out 0s 1";
    slides[nextSlide].style.animation = (nextSlide<currentSlide?"from_left":"from_right") + " " + animationTime + "s ease-in-out 0s 1";
    var tmpNext = nextSlide;
    var tmpCurr = currentSlide;
    window.setTimeout(function(){
        slides[tmpNext].style.display = "block";
        slides[tmpCurr].style.display = "none";
    }, animationTime*1000);
  } else {
    slides[currentSlide].style.display = "none";
    slides[nextSlide].style.display = "block";
  }
  currentSlide = nextSlide;
  $("#left").get(0).innerHTML = currentSlide>0?slides[currentSlide-1].children[0].innerHTML:"---";
  $("#right").get(0).innerHTML = currentSlide<slides.length-1?slides[currentSlide+1].children[0].innerHTML:"---";
}
// EINE KOSTPROBE JQUERY
toggleSlide2 = function(dir){
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
}

/*
document.body.onkeypress = function(e){
  switch(e.which){
    case 37: toggleSlide('left'); break;
    case 38: toggleSlide('right'); break;
    default: break;
  }
}*/
// = $(document).ready(prepSlides);
$(prepSlides);
