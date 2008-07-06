                <h2>Directories</h2>
                <ul id="tabmenu">
%if c.obj != '':
%if c.obj != c.root_dir:
                    <li>
                        <a href="/dir?path=${h.getBreadcrumbTrail(c.root_dir,c.obj)[-1].getPath()}">
                            <img src="/images/up.gif" alt="<-" border="0" />
                            Up one level
                        </a>
                    </li>
%endif
%if c.obj.getType() == "dir" and c.obj.getSubdirs():
%for dir in c.obj.getSubdirs():
                    <li class="tab">
                        <a href="/dir?path=${dir.getPath()}">
                            <img src="/images/dir.gif" border="0" alt="->" />
                            ${dir.getName()}
                        </a>
                    </li>
%endfor
%endif
%endif
                </ul>
