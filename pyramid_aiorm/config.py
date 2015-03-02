import asyncio
import logging
import importlib

from pyramid.events import subscriber, NewRequest
from pyramid.settings import aslist
from pyramid.tweens import EXCVIEW

import aiorm
from aiorm import orm
from aiorm import registry

log = logging.getLogger(__name__)


@asyncio.coroutine
def includeme(config):
    from aiorm.driver.postgresql.aiopg import Driver
    from aiorm.orm.dialect.postgresql import Dialect

    config.add_tween('pyramid_aiorm.transaction.tween_factory',
                     under=EXCVIEW)

    settings = {key:val for key, val in config.get_settings().items()
                if key.startswith('aiorm.')}
    driver_cls = settings.pop('aiorm.driver', 'aiorm.driver.postgresql.aiopg')
    driver_cls = getattr(importlib.import_module(driver_cls), 'Driver')
    registry.register(driver_cls)

    dialect = settings.pop('aiorm.driver', 'aiorm.orm.dialect.postgresql')
    dialect = importlib.import_module(dialect)
    dialect_cls = getattr(dialect, 'Dialect')
    registry.register(dialect_cls)
    dialect_cls = getattr(dialect, 'CreateTableDialect')
    registry.register(dialect_cls)

    ignored = len('aiorm.db.')
    for key, url in settings.items():
        if not key.startswith('aiorm.db.'):
            continue
        name = key[ignored:]
        yield from registry.connect(url, name=name)


    scanmods = aslist(settings['aiorm.scan'], flatten=True)
    for scanmod in scanmods:
        orm.scan(scanmod)
