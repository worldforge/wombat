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
            <td>Last changed:</td>
            <td>${c.obj.getLastChanged()}</td>
          </tr>
          <tr>
            <td>Direct Link:</td>
            <td><a href="/media/${c.obj.getPath()}">${c.obj.getPath()}</a></td>
          </tr>
        </table>
