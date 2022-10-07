# -*- coding: utf-8 -*-

from sqlalchemy.future import select
from hijim.common.db import use_db_session, with_db_session
from hijim.model.app import App


@use_db_session
async def get_mod_by_id(mod, _id):
    return await mod.get_by_id(_id)


@use_db_session
@with_db_session
async def get_app_by_name(name, *, session=None):
    result = await session.execute(select(App).filter(App.name == name))
    return result.scalars().all()


@use_db_session
async def delete_app_by_name(name):
    mods = await get_app_by_name(name)
    for mod in mods:
        await mod.delete()


@use_db_session
async def get_app_list():
    return await App.get_list()
