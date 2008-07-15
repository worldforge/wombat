<% g = 0 %>
%for group in  c.obj.getFilesByType():
%if group != []:
                    <div class="group">
                    	<h3>${group[0].getType().capitalize()} Files</h3>
<% i = 0 %>
                    	<div class="clr set">
%for file in group:
							<div id="item_${g}_${i}" class="lfloat item">
								<a href="/file?path=${file.getPath()}"
								   id="act_${g}_${i}"
								   title="View Details for: &ldquo;${file.getName()}&rdquo;"
								   type="text/itemDetail"
								   rel="/file/panel?path=${file.getPath()}">
									<img class="fade" src="/images/${file.getType()}.gif" border="0" alt="" />
									${file.getName()}<span class="meta">(${file.getPrettySize()})</span>
								</a>
								<!-- <small>(${file.getPrettySize()})</small> -->
								<div id="exp_item_${g}_${i}" class="exp"></div>
							</div>
<% i = i+1 %>
%endfor
	                   	</div>
                    </div>
%endif
<% g = g+1 %>
%endfor
