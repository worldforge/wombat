var revDetailsDisclosed = false;
var revAdvancedSearchDisclosed = false;

/**
  * wombat::init
  * Prepares the default state of the document including any settings stored in cookies.
  * @return	[nil]
  * @author	Thomas Ingham
  * @created	7/11/08 5:22 PM
 */
function init()
{
	var openByDefault = uncook('openRevDetails');
	if( openByDefault == "YES" )
	{
		revealDetails(0.1);
	}
}

/**
  * wombat::revealDetails
  * Toggles the display of the details panel for revisions.
  * @return	[nil]
  * @author	Thomas Ingham
  * @created	7/11/08 5:23 PM
 */
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

/**
  * wombat::revealAdvancedSearch
  * Toggles the display of the advanced search options
  * (copied from revealDetails with no cookies)
  * @return	[nil]
  * @author	Richard Flaherty
  * @created	7/13/08 2:27 PM
 */
function revealAdvancedSearch(speed)
{
	if( typeof(speed) == "undefined" ){ speed = 0.25; }
	if(revAdvancedSearchDisclosed)
	{
		Effect.SwitchOff('revAdvancedSearch',{duration:speed});
		revAdvancedSearchDisclosed = false;
	}
	else
	{
		Effect.BlindDown('revAdvancedSearch',{duration:speed});
		revAdvancedSearchDisclosed = true;
	}
}

/**
  * wombat::filterSearchResults
  * Extends the default search parameters by adding additional arguments.
  * Redirects the browser to the search results page.
  * @return	[nil]
  * @author		Thomas Ingham
  * @created	7/11/08 5:24 PM
 */
function filterSearchResults( query, author, dateIn, dateOut )
{
	//build new querystring and redirect the user.
	var url = "/show/search?match="+query+"&author="+author[author.selectedIndex].value+"&dateIn="+dateIn+"&dateOut="+dateOut;
	document.location.href = url;
}

/**
  * wombat::cook
  * Pickles a key value pair into the document cookie.
  * @return	[nil]
  * @author	Thomas Ingham
  * @created	7/11/08 5:23 PM
 */
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

/**
  * wombat::uncook
  * Retrieves a value from the document cookie by name.
  * @return	[String] The value for the matching key.
  * @author	Thomas Ingham
  * @created	7/11/08 5:24 PM
 */
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
