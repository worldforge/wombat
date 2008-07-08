%for group in  c.obj.getFilesByType():
%if group != []:
                    <div class="group">
                    	<h3>${group[0].getType().capitalize()} Files</h3>
	                    <table border="0" class="group">
	                      <tr>
<% i = 1 %>
%for file in group:
	                        <td class="cell" valign="top" width="50%">
	                            <a href="/file?path=${file.getPath()}" title="Download ${file.getName()}">
	                                <img class="fade" src="/images/${file.getType()}.gif" border="0" alt="*" />
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
<%i+=1%>
%endfor
	                      </tr>
	                    </table>
                    </div>
%endif
%endfor
