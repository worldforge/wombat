import logging

from wombat.lib.base import *
from pylons.decorators import validate
from wombat.model import Asset, Tag
from wombat.model.form import AssetForm

log = logging.getLogger(__name__)

class AssetController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Asset view'
        c.messages = []
        c.session = Session()

        c.assets = c.session.query(Asset).all()

        return render('/derived/asset/index.html')

    def show(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Asset view'
        c.messages = []

        if id is None:
            abort(404)
        c.session = Session()

        asset = c.session.query(Asset).get(id)
        if asset is None:
            abort(404)

        c.asset = asset

        return render('/derived/asset/show.html')

    def details(self, id):
        if id is None:
            abort(404)
        c.session = Session()

        asset = c.session.query(Asset).get(id)
        if asset is None:
            abort(404)

        c.asset = asset

        return render('/derived/asset/details.html')

    def new(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Add an asset'
        c.messages = []
        c.session = Session()

        return render('/derived/asset/new.html')

    def _create_tags_from_string(self, session, tag_string):
        tags = tag_string.split(u' ')
        tag_objects = []
        for tag in tags:
            if tag == u'':
                continue
            tag_obj = session.query(Tag).filter_by(name=tag).first()
            if tag_obj is None:
                # create a new tag
                tag_obj = Tag(tag)
                session.add(tag_obj)
            tag_objects.append(tag_obj)
        return tag_objects

    @validate(schema=AssetForm(), form="new")
    def create(self):
        session = Session()
        tag_string = self.form_result.get("asset_tags")
        tags = self._create_tags_from_string(session, tag_string)
        asset = Asset(self.form_result.get("asset_name"), tags)
        session.add(asset)
        session.commit()
        redirect_to(action="show", id=asset.id)

    def edit(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Edit Asset'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        c.asset = c.session.query(Asset).get(id)
        if c.asset is None:
            abort(404)

        return render('/derived/asset/edit.html')

    @validate(schema=AssetForm(), form="edit")
    def change(self, id):
        if id is None:
            abort(404)

        session = Session()

        asset = session.query(Asset).get(id)
        if asset is None:
            abort(404)

        asset.name = self.form_result.get("asset_name")
        tag_string = self.form_result.get("asset_tags")
        asset.tags = self._create_tags_from_string(session, tag_string)
        session.add(asset)
        session.commit()

        redirect_to(action="show", id=c.id)

    def delete(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Delete Asset'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        asset = c.session.query(Asset).get(id)
        if asset is None:
            abort(404)

        c.session.delete(asset)
        c.session.commit()

        return render('/derived/asset/delete.html')


