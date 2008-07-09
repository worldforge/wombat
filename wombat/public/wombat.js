var revDetailsDisclosed = false;

function init()
{
	var openByDefault = uncook('openRevDetails');
	if( openByDefault == "YES" )
	{
		revealDetails(0.1);
	}
}

function revealDetails(speed)
{
	if( typeof(speed) == "undefined" ){ speed = 0.25; }
	if(revDetailsDisclosed)
	{
		Effect.SwitchOff('revDetails',{duration:speed});
		revDetailsDisclosed = false;
		cook('openRevDetails','NO',10);
	}
	else
	{
		Effect.BlindDown('revDetails',{duration:speed});
		revDetailsDisclosed = true;
		cook('openRevDetails','YES',10);
	}
}

function cook(name,value,days)
{
	if(days)
	{
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function uncook(name)
{
	var nameIs = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameIs) == 0) return c.substring(nameIs.length,c.length);
	}
	return null;
}