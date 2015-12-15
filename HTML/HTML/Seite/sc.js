var mobile = false;

function load()
{

	document.getElementById('jsWarn').style.display = "none";

	window.setInterval('resize();', 200);

}

function resize()
{

	if(window.innerWidth < window.innerHeight){
		if(!mobile){
			mobile = true;
			document.getElementsByTagName('link')[0].href = 'mobile-st.css';
		}
	} 
	else{
		if(mobile){
			mobile = false;
			document.getElementsByTagName('link')[0].href = 'st.css';
		}
	}

}
