                <h2>Directories</h2>
                <ul id="tabmenu">
%if c.obj != '':
%if c.obj.getType() == "dir" and c.obj.getSubdirs():
%for dir in c.obj.getSubdirs():
                    <li class="tab">
                        <a href="/dir?path=${dir.getPath()}">${dir.getName()}</a>
                    </li>
%endfor
%else:
                    <li><a href="/dir?path=${h.getBreadcrumbTrail(c.root_dir,c.obj)[-1].getPath()}">Up one level</a></li>
%endif
%endif
                </ul>
