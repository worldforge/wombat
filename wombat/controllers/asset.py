import logging

from wombat.lib.base import *
from pylons.decorators import validate
from wombat.model import Asset
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

    @validate(schema=AssetForm(), form="new")
    def create(self):
        session = Session()
        asset = Asset(self.form_result.get("asset_name"),self.form_result.get("asset_keywords"))
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
        asset.keywords = self.form_result.get("asset_keywords")
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


