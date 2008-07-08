					<script language="javascript" type="text/javascript">
						var revDetailsDisclosed = false;
						function revealDetails()
						{
							if(revDetailsDisclosed)
							{
								Effect.Fade('revDetails');
								revDetailsDisclosed = false;
							}
							else
							{
								Effect.Appear('revDetails');
								revDetailsDisclosed = true;
							}
						}
					</script>
					<div class="breadcrumb block">
						<h3 onclick="revealDetails();">Revision Details</h3>
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
					</div>