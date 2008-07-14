var revDetailsDisclosed = false;
var revAdvancedSearchDisclosed = false;
var picker_date_in;
var picker_date_out;

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
	openByDefault = uncook('openSearch');
	if( openByDefault == "YES" )
	{
		revealAdvancedSearch(0.1);
	}
	picker_date_in = new Control.DatePicker('date_in', {icon: '/datepicker/calendar.png',dateFormat: 'yyyy-MM-dd'});
	picker_date_out = new Control.DatePicker('date_out', {icon: '/datepicker/calendar.png',dateFormat: 'yyyy-MM-dd'});
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
	var label = $("advSearchActivator");
	if( typeof(speed) == "undefined" ){ speed = 0.25; }
	if(revAdvancedSearchDisclosed)
	{
		Effect.SwitchOff('revAdvancedSearch',{duration:speed});
		Effect.Appear('searchbox',{duration:0.1});
		revAdvancedSearchDisclosed = false;
		label.innerText = "Advanced Search Options";
		cook('openSearch','NO',10);
	}
	else
	{
		Effect.BlindDown('revAdvancedSearch',{duration:speed});
		Effect.Fade('searchbox',{duration:0.1});
		revAdvancedSearchDisclosed = true;
		label.innerText = "<< Simple Search";
		cook('openSearch','YES',10);
	}
}

/**
 * wombat::clearAdvancedSearchForm
 * @return	[nil]
 * @author	tingham@coalmarch.com
 * @created	7/13/08 11:34 PM
 */
function clearAdvancedSearchForm()
{
	var form = $('advancedSearch');
	if( typeof(form) != "undefined" )
	{
		form.match.value = '';
		form.author.selectedIndex = 0;
		form.extension.selectedIndex = 0;
		form.date_in.value = '';
		form.date_out.value = '';
	}
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