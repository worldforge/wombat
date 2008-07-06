                <h2>Latest Additions</h2>
%if c.root_dir != '':
                <ul>
%for file in c.root_dir.getLatestAdditions():
	            <li>
                        <a href="/file?path=${file.getPath()}">
                            <img src="/images/${file.getType()}.gif" alt="*" border="0"/>
                            ${file.getName()}
                        </a>
                    </li>
%endfor
                </ul>
%endif
