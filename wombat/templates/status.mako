        <div id="status">
            <h3>Status</h3>
            <table class="details">
                <tr>
                    <td width="25%">Repository URL:</td>
                    <td><a href="${c.root_dir.getRepoUrl()}">${c.root_dir.getRepoUrl()}</a></td>
                </tr>
                <tr>
                    <td>Scan last performed:</td>
                    <td>${c.root_dir.getPrettyScanTime()}</td>
                </tr>
                <tr>
                    <td>Total size of the repository:</td>
                    <td>${c.root_dir.getPrettyTotalSize()}</td>
                </tr>
                <tr>
                    <td>Average file size:</td>
                    <td>${c.root_dir.getPrettyAvgFileSize()}</td>
                </tr>
                <tr>
                    <td>Most popular file type</td>
                    <td>${h.getMostPopularFile(c.root_dir)}</td>
                </tr>
            </table>
        </div>
