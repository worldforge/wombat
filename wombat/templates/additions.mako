                <h2>Latest Additions</h2>
%if c.root_dir != '':
                <ul>
%for file in c.root_dir.getLatestAdditions():
	            <li><a href="/file?path=${file.getPath()}">${file.getName()}</a></li>
%endfor
                </ul>
%endif
