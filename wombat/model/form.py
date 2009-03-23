import formencode

class AssetForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    asset_name = formencode.validators.UnicodeString(not_empty=True)
    asset_tags = formencode.validators.UnicodeString(not_empty=False)

class CollectionForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    collection_name = formencode.validators.UnicodeString(not_empty=True)
    collection_tags = formencode.validators.UnicodeString(not_empty=False)

