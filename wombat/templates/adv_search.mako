<form method="get" action="/show/search">
	<label>Search String</label>
	<input type="text" size="19" name="match" value="${c.needle}" />
	<label>Author</label>
	<select name="author">
		<optgroup label="Authors">
			<option value="">Anyone</option>
		%if c.root_dir != "":
			${h.rails.options_for_select(c.root_dir.getAuthors(), c.match_author)} 
		%endif
		</optgroup>
	</select>
	<label>Extension</label>
	<select name="extension">
		<optgroup label="Media Types">
			<option value="">Any Type</option>
		%if c.root_dir != "":
			${h.rails.options_for_select(c.root_dir.getExtensions(), c.match_ext)}
		%endif
		</optgroup>
	</select>
	<input type="submit" name="submit" value="Advanced Search"/>
</form>
