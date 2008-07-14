%for group in  c.obj.getFilesByType():
%if group != []:
                    <div class="group">
                    	<h3>${group[0].getType().capitalize()} Files</h3>
                    	<div class="clr set">
<% i = 1 %>
%for file in group:
							<div id="item_${i}"
								 class="lfloat item"
								 type="text/itemDetail"
								 rel="${file.getPath()">
									<a href="/file?path=${file.getPath()}"
									   title="Download ${file.getName()}">
										<img class="fade" src="/images/${file.getType()}.gif" border="0" alt="*" />
									</a>
									&nbsp;
									<a href="/file/?path=${file.getPath()}"
									   title="File details: ${file.getName()}">
										${file.getName()}
									</a>
									<small>(${file.getPrettySize()})</small>
							</div>
%endfor
	                   	</div>
                    </div>
%endif
%endfor
