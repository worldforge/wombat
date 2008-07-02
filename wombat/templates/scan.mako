<%inherit file="base.mako"/>
    <div id="main">

        <div class="subtitle">Scan the repository.</div>

        <div class="description">
%if h.canScan():
            <a href="/scan/scan">Scan</a> the repository. This can take quite
         some time.
%else:
            Scanning the repository is not necessary. Proceed to <a
             href="/dir">directory view</a>.
%endif
        </div>
    </div>
