var load = function()
{

	document.getElementById('jsWarn').style.display = "none";

	window.setInterval('resize();', 200);
}

var resize = function()
{

	if(window.innerWidth < window.innerHeight) 
		document.getElementsByTagName('link')[0].href = 'static/mobile-st.css';
	else 
		document.getElementsByTagName('link')[0].href = 'static/st.css';

}
