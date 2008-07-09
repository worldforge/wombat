                        <div class="breadcrumb block group">
                            <h3 class="lfloat">Navigation&nbsp;</h3>
%if c.obj != '' and c.root_dir != '':
                            <ul>
%for entry in h.getBreadcrumbTrail(c.root_dir, c.obj):
                                <li><a href="/dir?path=${entry.getPath()}"><img src="/images/dir.gif" border="0" alt="*" />&nbsp;${entry.getName()}</a>
%endfor
                                <li><img src="/images/${c.obj.getType()}.gif" border="0" alt="*" />&nbsp;${c.obj.getName()}</li>
                            </ul>
%else:
        Directory data not loaded.
%endif
                        </div>
