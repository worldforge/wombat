<%inherit file="base.mako"/>
                <div id="main">
                    <div class="block">
<%include file="nav.mako"/>
                    </div>

                    <div class="description">Viewing ${c.obj.getName()} directory.</div>

<%include file="dirlist.mako"/>
<%include file="filelist.mako"/>

                </div>
