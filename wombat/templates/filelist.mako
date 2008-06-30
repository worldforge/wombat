        <div class="group">Files</div>
        <table border="0" class="group">
          <tr>
          <% i = 0 %>
%for file in c.dir.getFiles():
            <td class="cell" valign="top" width="50%">
                <a href="/file?path=${file.getPath()}" title="Download ${file.getName()}">
                  <img class="fade" src="/images/text.gif" border="0" alt="*" />
                </a>
                &nbsp;
                <a href="/file/?path=${file.getPath()}" title="File details: ${file.getName()}">
                  ${file.getName()}
                </a>
                <small>(${file.getPrettySize()})</small>
            </td>
%if i%2 == 0:
          </tr>
          <tr>
%endif
%endfor
          </tr>
        </table>
