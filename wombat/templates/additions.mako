            <div class="heading">Latest Additions</div>
%if c.root_dir != '':
%for file in c.root_dir.getLatestAdditions():
                <a href="/file?path=${file.getPath()}">${file.getName()}</a>
%endfor
%endif
