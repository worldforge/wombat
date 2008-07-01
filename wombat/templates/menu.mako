            <ul id="tabmenu">
%if c.obj != '' and c.obj.getType() == "dir":
%for dir in c.obj.getSubdirs():
                <li class="tab">
                    <a href="/dir?path=${dir.getPath()}">${dir.getName()}</a>
                </li>
%endfor
%endif
            </ul>
