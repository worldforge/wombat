                    <table class="details">
                      <tr>
                        <td width="25%">Filename:</td>
                        <td>${c.obj.getName()}</td>
                      </tr>
                      <tr>
                        <td>Filesize:</td>
                        <td>${c.obj.getPrettySize()}</td>
                      </tr>
                      <tr>
                        <td>Last changed by:</td>
                        <td>${c.obj.getAuthor()}</td>
                      </tr>
                      <tr>
                        <td>Last changed at revision:</td>
                        <td>${c.obj.getRevision()}</td>
                      </tr>
                      <tr>
                        <td>Last changed on:</td>
                        <td>${c.obj.getDate()}</td>
                      </tr>
                      <tr>
                        <td>Last log message:</td>
                        <td>${c.obj.getLog()}</td>
                      </tr>
                      <tr>
                        <td>Direct Link:</td>
                        <td><a href="/media/${c.obj.getPath()}">${c.obj.getPath()}</a></td>
                      </tr>
                    </table>
