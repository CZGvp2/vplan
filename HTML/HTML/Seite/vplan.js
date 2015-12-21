var tabs = [
	document.getElementById('left'),
	document.getElementById('middle'),
	document.getElementById('right')
];

var currentTab = 1;

var update = function()
{
	for(i = 0; i < 3; i++)
		tabs[i].style.width = "0";
	tabs[currentTab].style.width = "100%";
}

var onSwipe = function(dir)
{
	if(currentTab <= 0 && dir == 'left' || currentTab >= 2 && dir == 'right') return;
	else{
		if(dir=='right') currentTab++;
		if(dir=='left') currentTab--;
		update();
	}
}