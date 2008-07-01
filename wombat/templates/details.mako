        <table class="details">
          <tr>
            <td width="25%">Filename:</td>
            <td>${c.file.getName()}</td>
          </tr>
          <tr>
            <td>Filesize:</td>
            <td>${c.file.getPrettySize()}</td>
          </tr>
          <tr>
            <td>Direct Link:</td>
            <td><a href="/media/${c.file.getPath()}">${c.file.getPath()}</a></td>
          </tr>
        </table>
