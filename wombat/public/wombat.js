var revDetailsDisclosed = false;
var revAdvancedSearchDisclosed = false;
var picker_date_in;
var picker_date_out;
var itemDetails = new Array();
var fileDetailsSpeed = 0.5;

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
	
	initItemDetails();
	initMessageDisposal();
	initRequiredFields();
}

/**
  * wombat::initItemDetails
  * Setups up item details in the page to disclose.
  * @return	[nil]
  * @author		Thomas Ingham
  * @created	7/14/08 6:33 PM
 */
function initItemDetails( )
{
	var elements = document.getElementsByTagName("a");
	for(var i=0;i<elements.length;i++)
	{
		var item = elements[i];
		//window.console.log("evaluating: "+item.id);
		if( item.getAttribute("type") != null )
		{
			if( item.getAttribute("type").indexOf("itemDetail") > -1 )
			{
				//window.console.log("preparing: "+item.id);
				item.onclick = function(evt)
				{
					var itemDetail = fetchItemDetail( this.getAttribute("rel") );
					var domId = itemDetail.domNode.id;
					//window.console.log("itemDetail "+itemDetail);
					if( itemDetail != null )
					{
						//window.console.log("clicked: "+domId);
						var subItem = "exp_"+domId.replace("act_","item_");
						var supItem = domId.replace("act_","item_");
						//window.console.log("supItem: "+supItem);
						if( itemDetail.visible )
						{
							Effect.BlindUp(subItem, {duration:fileDetailsSpeed/2, afterFinish: function(){
								$(supItem).className = $(supItem).className.replace("clr full","lfloat");
								$(subItem).innerHTML = "";
							}
							});
							itemDetail.visible = false;
							$(supItem).onclick = null;
						}
						else
						{
							var fetch = new Ajax.Request(
								itemDetail.fetchPath,
								{
									method:"get",
									onSuccess: function(transport)
									{
										var response = transport.responseText || "No Response.";							
										$(supItem).className = $(supItem).className.replace("lfloat","clr full");
										$(subItem).innerHTML = response;
										Effect.BlindDown(subItem, {duration:fileDetailsSpeed});
										itemDetail.visible = true;
										$(supItem).onclick = function(){ $(domId).onclick(); }
									},
									onFailure: function(){ alert("Failure Fetching File Details."); }
								}
							);
						}
					}
					return false;
				};
				
				var path = item.getAttribute("rel");
				item.setAttribute("href","javascript:void(0);");
				var newItem = {
								domNode: item,
								fetchPath: path,
								visible: false
							  };
				itemDetails[itemDetails.length] = newItem;
			}
		}
	}
	
}

/**
 * wombat::fetchItemDetail
 * @return	[itemDetail] The item detail whose fetchPath matches the requested path.
 * @author	tingham@coalmarch.com
 * @created	7/14/08 9:32 PM
 */
function fetchItemDetail( path )
{
	var i;
	for(i=0;i<itemDetails.length;i++)
	{
		//window.console.log("Item "+i+" Path: "+itemDetails[i].fetchPath);
		if( itemDetails[i].fetchPath == path )
		{
			return itemDetails[i];
		}
	}
	return null;
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

/**
  * wombat::initMessageDisposal
  * Fades the message box out after a time.
  * @return	[nil]
  * @author	Thomas Ingham
  * @created 9/18/08 10:14 PM
 */
function initMessageDisposal()
{
	var messageElement = $('message');
	if( messageElement )
	{
		Effect.Fade(messageElement,{duration:12.0,afterFinish:function(effect){ effect.element.remove(); }});
	}
}

/**
 * @function wombat:disclose
 * Hides and shows something by ID.
 * @author tingham
 * @created 9/18/08 11:29 PM
 **/
function disclose( id )
{
	var item = $(id);
	if( item )
	{
		if( item.style.display == "none" )
		{
			Effect.Appear(id);
		}
		else
		{
			Effect.Fade(id);
		}
	}
}

/**
 * @function wombat:initRequiredFields
 * Process required fields for proper hilighting.
 * @author tingham
 * @created 9/18/08 11:38 PM
 **/
function initRequiredFields()
{
	var elements = $$('div.req');
	elements.each( function(item)
		{
			var subitems = item.descendants();
			var input = subitems[1];
			if( input )
			{
				$(input).observe('focus',hilightRequiredFieldset);
				$(input).observe('blur',clearHilightRequiredFieldsets);
			}
		});
}

/**
 * @function wombat:hilightRequiredFieldset
 * @author tingham
 * @created 9/18/08 11:45 PM
 **/
function hilightRequiredFieldset( event )
{
	var element = event.element();
	clearHilightRequiredFieldsets();
	element.up().removeClassName("req");
	element.up().addClassName("reqd");
}

/**
 * @function wombat:clearHilightRequiredFieldsets
 * @author tingham
 * @created 9/18/08 11:54 PM
 **/
function clearHilightRequiredFieldsets()
{
	var elements = $$('div.reqd');
	elements.each( function(item)
		{
			item.removeClassName("reqd");
			item.addClassName("req");
		});
}