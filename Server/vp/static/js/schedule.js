// Alle Slides müssen ein vorgefertigtes Style-setup bekommen:
prepSlides = function(){
  var slides = $(".slide");
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentSlide?"block":"none";
  $("#left").get(0).innerHTML = currentSlide>0?slides[currentSlide-1].children[0].innerHTML:"---";
  $("#right").get(0).innerHTML = currentSlide<slides.length-1?slides[currentSlide+1].children[0].innerHTML:"---";
}

max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }
// "harte" Übergänge: aus- und einblenden statt blenden nach links und rechts;
// funktioniert so aber immerhin
toggleSlide = function(dir){
  var slides = $(".slide");
  if(slides.length <= 1) return;
  var nextSlide = dir=="left"?max(currentSlide-1, 0):min(currentSlide+1,slides.length-1);
  console.log("[DEBUG] SlideEvent // old:" + currentSlide + " new:" + nextSlide);
  // hier könnte man mit css3 transitions u. animations nen schönen Übergang bauen
  if(nextSlide!=currentSlide){
    for(var i = 0; i < slides.length; i++) slides[i].style.display = "none";
    slides[nextSlide].style.display = slides[currentSlide].style.display = "block";
    slides[currentSlide].style.animation = (nextSlide>currentSlide?"fade_left":"fade_right") + " 1s ease-out 0s 1";
    slides[nextSlide].style.animation = (nextSlide<currentSlide?"from_left":"from_right") + " 1s ease-out 0s 1";
    window.setTimeout(function(){
      slides[nextSlide].style.display = "none";
        slides[currentSlide].style.display = "none";
    }, 1000);
  } else {
    slides[currentSlide].style.display = "none";
    slides[nextSlide].style.display = "block";
  }
  currentSlide = nextSlide;
  $("#left").get(0).innerHTML = currentSlide>0?slides[currentSlide-1].children[0].innerHTML:"---";
  $("#right").get(0).innerHTML = currentSlide<slides.length-1?slides[currentSlide+1].children[0].innerHTML:"---";
}
/*
document.body.onkeypress = function(e){
  switch(e.which){
    case 37: toggleSlide("left"); break;
    case 38: toggleSlide("right"); break;
    default: break;
  }
}*/
// = $(document).ready(prepSlides);
$(prepSlides);
