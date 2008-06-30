<%inherit file="base.mako"/>
    <div id="main">
        <div class="block">
<%include file="nav.mako"/>
        </div>
        <div class="block">
<%include file="additions.mako"/>
        </div>

        <div class="subtitle">Welcome to ${c.name}.</div>

        <div class="description">In some later version, this page will show some
        status information.<br />
        For now, just proceed to the <a href="/dir">directory view</a> page.</div>
    </div>
