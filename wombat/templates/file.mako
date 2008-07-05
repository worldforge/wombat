<%inherit file="base.mako"/>
    <div id="main">
        <div class="block">
<%include file="nav.mako"/>
        </div>

        <div class="subtitle">${c.obj.getName()}</div>

        <div class="description">Viewing ${c.obj.getName()}.</div>

<%include file="details.mako"/>
<%include file="pagination.mako"/>

    </div>
