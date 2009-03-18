import logging

from wombat.lib.base import *
from pylons.decorators import validate
from wombat.model import Collection
from wombat.model.form import CollectionForm


log = logging.getLogger(__name__)

class CollectionController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'All Collections'
        c.messages = []
        c.session = Session()

        c.collections = c.session.query(Collection).all()

        return render('/derived/collection/index.html')

    def show(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Collection view'
        c.messages = []

        if id is None:
            abort(404)
        c.session = Session()

        c.collection = c.session.query(Collection).get(id)
        if c.collection is None:
            abort(404)

        return render('/derived/collection/show.html')

    def details(self, id):
        if id is None:
            abort(404)
        c.session = Session()

        c.collection = c.session.query(Collection).get(id)
        if c.collection is None:
            abort(404)

        return render('/derived/collection/details.html')

    def new(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Add a Collection'
        c.messages = []
        c.session = Session()

        return render('/derived/collection/new.html')

    @validate(schema=CollectionForm(), form="new")
    def create(self):
        session = Session()
        collection = Collection(self.form_result.get("collection_name"),self.form_result.get("collection_keywords"))
        session.add(collection)
        session.commit()
        redirect_to(action="show", id=collection.id)

    def edit(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Edit Collection'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        c.collection = c.session.query(Collection).get(id)
        if c.collection is None:
            abort(404)

        return render('/derived/collection/edit.html')

    @validate(schema=CollectionForm(), form="edit")
    def change(self, id):
        if id is None:
            abort(404)

        session = Session()

        collection = session.query(Collection).get(id)
        if collection is None:
            abort(404)

        collection.name = self.form_result.get("collection_name")
        collection.keywords = self.form_result.get("collection_keywords")
        session.add(collection)
        session.commit()

        redirect_to(action="show", id=c.id)

    def delete(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Delete Collection'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        collection = c.session.query(Collection).get(id)
        if collection is None:
            abort(404)

        c.session.delete(collection)
        c.session.commit()

        return render('/derived/collection/delete.html')


