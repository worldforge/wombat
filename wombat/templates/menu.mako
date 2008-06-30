            <ul id="tabmenu">
%if c.dir != '':
%for dir in c.dir.getSubdirs():
                <li class="tab">
                    <a href="/dir?path=${dir.getPath()}">${dir.getName()}</a>
                </li>
%endfor
%endif
            </ul>
