import logging

from wombat.lib.base import *
from pylons.decorators import validate
from wombat.model import Collection, Tag
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

    @validate(schema=CollectionForm(), form="new")
    def create(self):
        session = Session()
        tag_string = self.form_result.get("collection_tags")
        tags = self._create_tags_from_string(session, tag_string)
        collection = Collection(self.form_result.get("collection_name"), tags)
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
        tag_string = self.form_result.get("collection_tags")
        collection.tags = self._create_tags_from_string(session, tag_string)
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


