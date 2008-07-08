					<script language="javascript" type="text/javascript">
					<![CDATA[
						var revDetailsDelimited = false;
						function revealDetails()
						{
							if(revDetailsDelimited)
							{
								Effect.Fade('revDetails');
							}
							else
							{
								Effect.Appear('revDetails');
							}
						}
					]]>
					</script>
					<h2 onclick="revealDetails();">Revision Details</h2>
					<div id="revDetails"
						 style="display:none;">
						<table class="details">
						  <tr>
							<td width="25%">Revision:</td>
							<td>${c.obj.getRev()}</td>
						  </tr>
						  <tr>
							<td>Last changed by:</td>
							<td>${c.obj.getLastChangedAuthor()}</td>
						  </td>
						  <tr>
							<td>Last changed at revision:</td>
							<td>${c.obj.getLastChangedRev()}</td>
						  </tr>
						  <tr>
							<td>Last changed on:</td>
							<td>${c.obj.getLastChangedDate()}</td>
						  </tr>
						</table>
					</div>