<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 TRANSITIONAL//EN">
<html>
<head>
    <title>${c.name} - ${c.title}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="/stylesheet.css">
    <link rel="shortcut icon" href="/favicon.ico">
</head>
<body>
    <table id="top" cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td>
          <div id="logo">
            <a href="index">
              <img src="/images/headerlogo.png" border="0" id="logo" title="${c.name}" />
            </a>
          </div>
<%include file="searchbox.mako"/>
        </td>
      </tr>
      <tr>
        <td id="menu">
<%include file="menu.mako"/>
        </td>
      </tr>
    </table>

<%include file="messages.mako"/>

    ${next.body()}

    <div id="bottom">
        <a href="http://wiki.worldforge.org/wiki/Wombat">WorldForge Open Mediai
	Browser/Archive Tool (WOMBAT) ${g.version}</a> &copy; 2008  Kai Blin<br />
        The copyrights of the contents of this page are held by the respective
        creators.
    </div>
</body>
</html>

