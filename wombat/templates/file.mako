<%inherit file="base.mako"/>
    <div id="main">
        <div class="block">
<%include file="nav.mako"/>
        </div>

        <div class="subtitle">${c.file.getName()}</div>

        <div class="description">Viewing ${c.file.getName()}.</div>

<%include file="details.mako"/>
<%include file="pagination.mako"/>
<%include file="comments.mako"/>

    </div>
