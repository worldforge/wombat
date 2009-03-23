#!/bin/bash
DB=${1}
BACKUP_PREFIX=${2}

sqlite3 ${DB} ".dump revisions" > ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump dirs" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump files" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump assets" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump collections" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump tags" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump asset_tags" >> ${BACKUP_PREFIX}_content.sql
sqlite3 ${DB} ".dump collection_tags" >> ${BACKUP_PREFIX}_content.sql

sqlite3 ${DB} ".dump users" > ${BACKUP_PREFIX}_meta.sql
sqlite3 ${DB} ".dump user_data" >> ${BACKUP_PREFIX}_meta.sql
sqlite3 ${DB} ".dump roles" >> ${BACKUP_PREFIX}_meta.sql
sqlite3 ${DB} ".dump user_roles" >> ${BACKUP_PREFIX}_meta.sql
sqlite3 ${DB} ".dump email_confirm" >> ${BACKUP_PREFIX}_meta.sql
sqlite3 ${DB} ".dump reset_data" >> ${BACKUP_PREFIX}_meta.sql
