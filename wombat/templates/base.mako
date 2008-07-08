<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>${c.name} - ${c.title}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="/stylesheet.css" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <script language="javascript" type="text/javascript" src="/scriptaculous/prototype.js" />
    <script language="javascript" type="text/javascript" src="/scriptaculous/scriptaculous.js?load=effects" />
</head>
<body>
    <div id="root">
        <div id="header">
            <div id="logo">
                <a href="/" title="${c.name}">
                    <img src="/images/headerlogo.png"
                    	 border="0"
                    	 alt="${c.name}" />
                </a>
            </div>
            <div id="logo-text">${c.name}</div>
            <div id="search">
<%include file="searchbox.mako"/>
	    </div>
        </div>
        <div id="middle">
            <div id="menu">
<%include file="menu.mako"/>
<%include file="additions.mako"/>
	    </div>
	    <div id="content">
<%include file="messages.mako"/>
${next.body()}
	    </div>
        </div>
    </div>
    <div id="footer">
        <a href="http://wiki.worldforge.org/wiki/Wombat">WorldForge Open Mediai Browser/Archive Tool (WOMBAT)
        ${g.version}</a> &copy; 2008  Kai Blin<br />
        The copyrights of the contents of this page are held by the respective creators.
    </div>
</body>
</html>

