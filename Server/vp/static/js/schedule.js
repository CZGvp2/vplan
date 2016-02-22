var currentSlide = 0; // Irgendwie muss das dann am anfang der Index von der Slide von heute sein

// Alle Slides müssen ein vorgefertigtes Style-setup bekommen:
prepSlides = function(){
  var slides = $(".slide");
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentSlide?"block":"none";
}

max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }
// "harte" Übergänge: aus- und einblenden statt blenden nach links und rechts;
// funktioniert so aber immerhin
toggleSlide = function(dir){
  var slides = $(".slide");
  if(slides.length <= 1) return;
  var nextSlide = dir=="left"?max(currentSlide-1, 0):min(currentSlide+1,slides.length-1);
  console.log("cr:" + currentSlide + " n:" + nextSlide);
  // hier könnte man mit css3 transitions u. animations nen schönen Übergang bauen
  slides[currentSlide].style.display = "none";
  slides[nextSlide].style.display = "block";
  currentSlide = nextSlide;
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
