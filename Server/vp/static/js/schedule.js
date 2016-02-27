// Filter functions
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

// Cookie functions
setCookie = function(attrib, value, exp_days) {
  var d = new Date();
  d.setTime(d.getTime() + (exp_days*24*60*60*1000));
  document.cookie = attrib + "=" + value + "; expires=" + d.toUTCString();
}

getCookie = function(attrib){
  var split_cookie = document.cookie.split("; ");
  attrib+="=";
  for(var i=0; i<split_cookie.length; i++)
    if(split_cookie[i].indexOf(attrib) == 0)
      return split_cookie[i].substring(attrib.length,split_cookie[i].length);
  return "";
}

removeCookie = function(attrib){
  setCookie(attrib, "", -1);
}


var currentIndex = 0;

// Setup function
setup = function(){
  filter(getCookie("class"));
  $("#fixedHeader").hide();
  setSidebars(currentIndex, $(".slide"));
  var slides = $('.slide');
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentIndex?'block':'none';
  $('#left').get(0).innerHTML = currentIndex>0?slides[currentIndex-1].children[0].innerHTML:'---';
  $('#right').get(0).innerHTML = currentIndex<slides.length-1?slides[currentIndex+1].children[0].innerHTML:'---';
}

// Quick access to Math-Package functions
max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }

var animationTime = 0.5;
var t_out = -1;

// Function to allow sliding between different days
// Argument: "left" or "right"
toggleSlide = function(dir){
  var slides = $(".slide"); // <- jQuery
  if(slides.length <= 1 || t_out >= 0) return;
  var nextIndex = dir=="left"?max(currentIndex-1, 0):min(currentIndex+1,slides.length-1);
  if(nextIndex!=currentIndex){
    scrollTo(0,0);
    onScroll(0);
    for(var i = 0; i < slides.length; i++) slides[i].style.display = "none";
    slides[nextIndex].style.display = slides[currentIndex].style.display = "block";
    slides[currentIndex].style.animation = (nextIndex>currentIndex?"fade_left":"fade_right") + " " + animationTime + "s ease-in-out 0s 1";
    slides[nextIndex].style.animation = (nextIndex<currentIndex?"from_left":"from_right") + " " + animationTime + "s ease-in-out 0s 1";
    var tmpNext = nextIndex;
    var tmpCurr = currentIndex;
    slides[tmpNext].style.display = "block";
    t_out = window.setTimeout(function(){
        slides[tmpCurr].style.display = "none";
        t_out = -1;
    }, animationTime*1000);
  } else {
    slides[currentIndex].style.display = "none";
    slides[nextIndex].style.display = "block";
  }
  currentIndex = nextIndex;
  setSidebars(currentIndex, slides);
}

setSidebars = function(idx, slides){
  if(idx>0){
    $("#leftslidebutton").show();
    $("#left").text($(slides[idx-1]).find(".slide_title").text());
  } else $("#leftslidebutton").hide();
  if(idx<slides.length-1){
    $("#rightslidebutton").show();
    $("#right").text($(slides[idx+1]).find(".slide_title").text());
  } else $("#rightslidebutton").hide();
}

onScroll = function(evt){
  if(typeof evt == 'number') $("#fixedHeader").hide();
  else{
    evt.preventDefault();
    if(scrollY > $("#wrapper").height() - $("#fixedHeader").height() - 20 && !show_f_h){
      $("#fixedHeader").fadeIn(animationTime*1000*0.5);
      show_f_h = true;
    }
    else if(scrollY < $("#wrapper").height() - $("#fixedHeader").height() - 20 && show_f_h){
      $("#fixedHeader").fadeOut(animationTime*1000*0.5);
      show_f_h = false;
    }
  }
}

toggleMenue = function(){
  console.log("Menue button clicked");
  removeFilter();
}

// Add keylistener to toggle slides via arrow keys
$(document).on('keypress', function(evt){
  switch(evt.keyCode){
    case 37:
      toggleSlide('left');
      evt.preventDefault();
      evt.stopPropagation();
      break;
    case 39:
      toggleSlide('right');
      evt.preventDefault();
      evt.stopPropagation();
      break;
  }
});

var show_f_h = false;
// Catch Scrollevents, show or hide header
$(document).on('scroll', onScroll);

// Call setup() when DOM is ready
$(setup);
