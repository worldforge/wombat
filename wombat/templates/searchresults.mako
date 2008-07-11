<%inherit file="base.mako"/>
    <div class="clr group">
    	<em>Found ${len(c.found_dirs)} directories and ${len(c.found_files)} files containing "${c.needle | h}".</em>
		
<%
	authors = c.root_dir.getAuthors()
	selectedAuthor = "None loaded";
%>
%if authors != []:
			<form name="authorFilterForm" action="/" method="get" onsubmit="return false;">
				<label for="authors">Filter Your Results By Author:</label>
				<select name="authors" id="authors" onchange="filterSearchResults('${c.needle}',this,'','');">
					<option value="">Authors</option>
%for auth in authors:
					<option value="${auth}"
%if selectedAuthor == auth:
							selected="selected"
%endif
					>${auth}</option>
%endfor
				</select>
			</form>
%endif

%if c.found_dirs != []:
        <table border="0" class="group">
          <tr>
          <% i = 0 %>
%for dir in c.found_dirs:
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
%endif

%if c.found_files != []:
		<h3>Found Files</h3>
        <table border="0" class="group">
          <tr>
          <% i = 0 %>
%for file in c.found_files:
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
<%i+=1%>
%if i%2 == 0:
          </tr>
          <tr>
%endif
%endfor
          </tr>
        </table>
%endif

    </div>
