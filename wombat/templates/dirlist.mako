        <table border="0" class="dirs">
          <tr>
          <% i = 0 %>
%for dir in c.obj.getSubdirs():
            <td class="cell" valign="top" width="50%">
                <a href="/dir?path=${dir.getPath()}" title="${dir.getName()}">
                  <img class="fade" src="/images/dir.gif" border="0" alt="*" />
                  &nbsp;${dir.getName()}&nbsp;<small>(${len(dir.getSubdirs())} subdirs &nbsp;
                  ${len(dir.getFiles())} files)</small><br />
                </a>
            </td>
            <% i += 1%>
%if i%2 == 0:
          </tr>
          <tr>
%endif
%endfor
          </tr>
        </table>
