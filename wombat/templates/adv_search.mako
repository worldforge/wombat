<form method="get" action="/show/search">
	<label>Search String</label>
	<input type="text" size="19" name="match" value="${c.needle}" />
	<label>Author</label>
	<select name="author">
		<option value=></option>
		%if c.root_dir != "":
			${h.rails.options_for_select(c.root_dir.getAuthors())} 
		%endif
	</select>
	<label>Extension</label>
	<select name="extension">
		%if c.root_dir != "":
			${h.rails.options_for_select(c.root_dir.getExtensions())}
		%endif
	</select>
	<input type="submit" name="submit" value="Advanced Search"/>
</form>
