/*
* SCHEDULE.JS
*
* 1. Filter slides for a target query
* 2. Read, write and remove Cookies
* 3. Handle slides and corresponding keyEvents
* 4. setup DOM once everything is built by the client
*
*/

//vars
var currentIndex = 0;
var animationTime = 0.5;
var t_out = -1;
var show_f_h = false;


showEmptyMessage = function(slide){
	if($(slide).find(".event:visible").length==0) $(slide).find(".empty_msg").show();
	else $(".empty_msg").hide();
}

// Filter functions
filter = function(target) {
    var events = $('.event');
    if(target){
        for(var i=0; i < events.length; i++){
            var e = $(events[i]);
            var targets = e.data().targets.toLowerCase()/*.split(' ')*/;
            if (!~targets.indexOf(target.toLowerCase())) e.hide();
            else e.show();
        }
    } else events.show();
	  showEmptyMessage($(".slide").get(currentIndex));
		if(target) $(".selector").fadeOut(animationTime*1000*0.3);
		else $(".selector").fadeIn(animationTime*1000*0.3);
}

removeFilter = function(){
    $('.event').show();
    showEmptyMessage($(".slide").get(currentIndex));
}

// Cookie functions
setCookie = function(attrib, value, exp_days) {
  var d = new Date();
  d.setTime(d.getTime() + (exp_days*24*60*60*1000));
	// ich hab mal path=/ als standard dringelassen, müssen wir dasfür irgendwas ändern?
  document.cookie = attrib + "=" + value + "; expires=" + d.toUTCString();
}

getCookie = function(attrib){
  var split_cookie = document.cookie.split("; ");
  attrib+="=";
  for(var i=0; i<split_cookie.length; i++)
    if(~split_cookie[i].indexOf(attrib))
      return split_cookie[i].substring(attrib.length + split_cookie[i].indexOf(attrib),split_cookie[i].length);
  return "";
}

removeCookie = function(attrib){
  setCookie(attrib, "", -1);
}

// Setup function
setup = function(){
  filter(getCookie("class"));
  $("#fixedHeader").hide();
	$(".empty_msg").hide();
	$("#jsWarn").hide();
  if(getCookie("class")) toggleFilterbutton();
  setSidebars(currentIndex, $(".slide"));
	showEmptyMessage($(".slide").get(currentIndex));
  $('#input').val(getCookie('class'));
	// "Debug" function
	if(getCookie("philip").indexOf('q')==0){
		if(getCookie("philip").substring(1)) alert(getCookie("philip").substring(1));
		$("body").css("background-image","linear-gradient(90deg, yellow, red, purple, blue, green, yellow)");
	}
  if(getCookie("gradient").indexOf('yes')==0){
    $(".sub_subject, .sub_subject_2").css("background-image", "linear-gradient(to bottom, rgba(0,0,0,0) 40%, white 160%)");
    $("#header").css("background-image", "linear-gradient(to bottom, #0e0e0e 0%, rgba(0,0,0,0) 20%)");
  }
  var slides = $('.slide');
  for(var i = 0; i < slides.length; i++)
    slides[i].style.display = i==currentIndex?'block':'none';
  $('#left').get(0).innerHTML = currentIndex>0?slides[currentIndex-1].children[0].innerHTML:'---';
  $('#right').get(0).innerHTML = currentIndex<slides.length-1?slides[currentIndex+1].children[0].innerHTML:'---';
}

// Quick access to Math-Package functions
max = function(i, j){ return Math.max(i, j); }
min = function(i, j){ return Math.min(i, j); }

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
	showEmptyMessage(slides[currentIndex]);
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

toggleVisibility = function(obj){
  if(obj.style.display == "none"){$(obj).fadeIn(animationTime*1000*0.2); return true;}
  else $(obj).fadeOut(animationTime*1000*0.2);
  return false;
}
/*
* Listener functions
*/
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

toggleMenu = function(time = animationTime*1000*0.5){
  if(toggleVisibility($("#menuContainer")[0])) $("#cover").fadeIn(time);
  /*if(shown){
    $("#topbar").css("background-color", "#3a7ab6");
    $("#header").css("background-image", "linear-gradient(to bottom, #3a7ab6 0%, rgba(0,0,0,0) 70%)");
  } else {
    $("#topbar").css("background-color", "");
    $("#header").css("background-image", "");
  }*/
}

toggleFilter = function(value){
  if(!value) removeCookie("class");
	else setCookie("class", value, 100);
	filter(value);
}

toggleFilterbutton = function(){
  var b = $("#toggleFilterButton")[0];
  if(toggleVisibility($("#filterBox").get(0)))
    b.innerHTML = 'Filter deaktivieren';
  else{
    b.innerHTML = 'Filter aktivieren';
    toggleFilter('');
    $('input').val('');
  }
}

toggleDropdown = function(evt){

}

$(function(){
  // Add listener to update filter and cookie when input is changed
  $("#input").on('keyup keypress paste', function(evt){
  	toggleFilter($('#input').val());
  });

  // Add menu Listener
  $("#menuSpace, .menuButton").on('click', toggleMenu);
  $("#cover").on('click', function(){
    toggleMenu();
    $("#cover").fadeOut(animationTime*1000*0.5);
  });

  toggleMenu(0);
});

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

// Catch Scrollevents, show/hide header if necessary
$(document).on('scroll', onScroll);

//Catch swipes
$(function(){
	$(document).tactile({
		left: function(){toggleSlide("left")},
		right: function(){toggleSlide("right")}
	});
});


// Call setup() when DOM is ready
$(setup);

/**
JAVASCRIPT CHALLENGE #1
r = Math.random;
var x = (...p)=>((r()*(p[~-1]-p[+!0]+~-2))+p[~-2])>>+!1;

Welchen Wert hat x?
Was passiert bei 'x(1,10);'?
*/
