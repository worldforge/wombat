//Lazy Loading Script
//By Evan Blum

//Any elements that are lazy-loaded will only be loaded when they are on screen.
//Items may not be added to the lazy-load queue after the onLoad event
//You must call layout() every time you change the position of the items.

//PUBLIC ------------
//Adds an element to the list of items to be lazy-loaded. Takes a url to
//send a request to, and an element to update with the results. The
//request is only sent when the element is in view.
function lazyLoad(path, element) {
	itemsToLoad.push(new lazyLoadItem(path, element));
}


//PRIVATE ------------
//Initialize an array of items to be lazy-loaded; this is updated by the
//lazyLoad function
itemsToLoad = new Array();

//A class that contains the path of the request, the element to
//update,and a generated function to update it
function lazyLoadItem(path, element) {
	this.path=path;
	this.element=element;
	this.offsetTop = undefined;
	this.load=function(){
		new Ajax.Updater({success: this.element },path,{
			onComplete: nextRequest});

	}
}

//returns 1 if element is in the viewport, 0 otherwise
function isInView(element) {
	var viewportTop =element.viewportOffset()[1];
	return (viewportTop > 0 && viewportTop < document.viewport.getHeight())
}

//This function determines the next lazyLoadItem to load and calls its
//load method, or sets a timeout to try again if all onscreen elements are loaded
function nextRequest(){
	if (!itemsToLoad.length) {
		return; //EXIT POINT -- Everyting is loaded.
	}
	var nextItem;
	var nextItemIndex;
	var viewportTop = document.viewport.getScrollOffsets()[1] - 200;
	var viewportBottom = document.viewport.getHeight() + viewportTop + 200;
	for (var i = 0, len = itemsToLoad.length; i < len; ++i) {
		var item = itemsToLoad[i];
		if (viewportTop < item.offsetTop && item.offsetTop < viewportBottom)
		{
			nextItem = item;
			nextItemIndex = i;
			itemsToLoad.splice(i,1);
			break;
		}
	}
	if (nextItem) {
		nextItem.load();
	}
	else {
		setTimeout("nextRequest();",500);
	}
}

function layout()
{
	if (!itemsToLoad.length) {
		return;
	}
	for (var i = 0, len = itemsToLoad.length; i < len; ++i) {
		var item = itemsToLoad[i];
		if (!item.offsetTop)
		{
			item.offsetTop = item.element.cumulativeOffset().top
		}
	}
}

function lazyLoad_startup()
{
	layout();
	nextRequest();
}
Event.observe(window, 'load', lazyLoad_startup);
