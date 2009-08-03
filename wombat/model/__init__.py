"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from wombat.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.sa.Table("Foo", meta.metadata,
#    sa.sa.Column("id", sa.sa.types.Integer, primary_key=True),
#    sa.sa.Column("bar", sa.sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
from revision import Revision, init_rev_table
rev_table = init_rev_table(meta.metadata)

from file import File, init_files_table
files_table = init_files_table(meta.metadata)

from dir import Dir, init_dirs_table
dirs_table = init_dirs_table(meta.metadata)

from asset import Asset, init_assets_table
assets_table = init_assets_table(meta.metadata)

from collection import Collection, init_collections_table
collections_table = init_collections_table(meta.metadata)

from user import User, init_users_table
users_table = init_users_table(meta.metadata)

from user_data import UserData, init_user_data_table
user_data_table = init_user_data_table(meta.metadata)

from role import Role, init_roles_table
roles_table = init_roles_table(meta.metadata)

from tag import Tag, init_tags_table
tags_table = init_tags_table(meta.metadata)

user_roles = sa.Table('user_roles', meta.metadata,
        sa.Column('user_id', sa.types.Integer, sa.ForeignKey('users.id')),
        sa.Column('role_id', sa.types.Integer, sa.ForeignKey('roles.id'))
        )

asset_tags = sa.Table('asset_tags', meta.metadata,
        sa.Column('asset_id', sa.types.Integer, sa.ForeignKey('assets.id')),
        sa.Column('tag_id', sa.types.Integer, sa.ForeignKey('tags.id'))
        )

collection_tags = sa.Table('collection_tags', meta.metadata,
        sa.Column('collection_id', sa.types.Integer, sa.ForeignKey('collections.id')),
        sa.Column('tag_id', sa.types.Integer, sa.ForeignKey('tags.id'))
        )

files_queues = sa.Table('files_queues', meta.metadata,
        sa.Column('file_path', sa.types.Unicode(255), sa.ForeignKey('files.path')),
        sa.Column('queue_id', sa.types.Integer, sa.ForeignKey('download_queues.id'))
        )

from reset_data import ResetData, init_reset_data_table
reset_data_table = init_reset_data_table(meta.metadata)

from email_confirm import EmailConfirm, init_email_confirm_table
email_confirm_table = init_email_confirm_table(meta.metadata)

from download_queue import DownloadQueue, init_download_queue_table
download_queue_table = init_download_queue_table(meta.metadata)

from upload import Upload, init_uploads_table
uploads_table = init_uploads_table(meta.metadata)

orm.mapper(Upload, uploads_table)
orm.mapper(File, files_table)
orm.mapper(Dir, dirs_table, properties={
    "files":orm.relation(File, backref="directory"),
    "subdirs":orm.relation(Dir, backref=orm.backref("parent", remote_side=[dirs_table.c.path]))})
orm.mapper(Revision, rev_table, properties={
    "files":orm.relation(File, backref="revision"),
    "dirs":orm.relation(Dir, backref="revision")})
orm.mapper(Asset, assets_table, properties={
    "files":orm.relation(File, backref="asset")})
orm.mapper(Collection, collections_table, properties={
    "assets":orm.relation(Asset, backref="collection")})
orm.mapper(User, users_table)
orm.mapper(UserData, user_data_table, properties={
    "user":orm.relation(User, backref=orm.backref("user_data", uselist=False),
                    single_parent=True, cascade="all, delete, delete-orphan")})
orm.mapper(Role, roles_table, properties={
    "users":orm.relation(User, secondary=user_roles, backref="roles",
                    cascade="all, delete")})
orm.mapper(Tag, tags_table, properties={
    "assets":orm.relation(Asset, secondary=asset_tags, backref="tags",
                    cascade="all, delete"),
    "collections":orm.relation(Collection, secondary=collection_tags, backref="tags",
                    cascade="all, delete")})
orm.mapper(ResetData, reset_data_table)
orm.mapper(EmailConfirm, email_confirm_table)
orm.mapper(DownloadQueue, download_queue_table, properties={
    "user":orm.relation(User, backref=orm.backref("download_queue", uselist=False),
                    single_parent=True, cascade="all, delete, delete-orphan"),
    "files":orm.relation(File, secondary=files_queues, backref="in_queues")})


