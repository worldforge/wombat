            <div class="heading">Latest Additions</div>
%for file in c.root_dir.getLatestAdditions():
                <a href="/file?path=${file.getPath()}">${file.getName()}</a>
%endfor
