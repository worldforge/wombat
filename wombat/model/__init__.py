from pylons import config
from sqlalchemy import Column, MetaData, Table, types, schema
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
                                      bind=config['pylons.g'].sa_engine))

metadata = MetaData()

from revision import Revision, init_rev_table
rev_table = init_rev_table(metadata)

from file import File, init_files_table
files_table = init_files_table(metadata)

from dir import Dir, init_dirs_table
dirs_table = init_dirs_table(metadata)

from asset import Asset, init_assets_table
assets_table = init_assets_table(metadata)

from collection import Collection, init_collections_table
collections_table = init_collections_table(metadata)

from user import User, init_users_table
users_table = init_users_table(metadata)

mapper(File, files_table)
mapper(Dir, dirs_table, properties={
    "files":relation(File, backref="directory"),
    "subdirs":relation(Dir, backref=backref("parent", remote_side=[dirs_table.c.path]))})
mapper(Revision, rev_table, properties={
    "files":relation(File, backref="revision"),
    "dirs":relation(Dir, backref="revision")})
mapper(Asset, assets_table, properties={
    "files":relation(File, backref="asset")})
mapper(Collection, collections_table, properties={
    "assets":relation(Asset, backref="collection")})
mapper(User, users_table)

