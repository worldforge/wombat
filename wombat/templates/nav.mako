            <div class="heading">Navigation</div>
%for entry in h.getBreadcrumbTrail(c.root_dir, c.obj):
            <a href="/dir?path=${entry.getPath()}"><img src="/images/dir.gif"
            border="0" alt="*" />&nbsp;${entry.getName()}</a>
%endfor
