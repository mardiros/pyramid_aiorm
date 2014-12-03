import asyncio
import logging

from aiorm import orm
from pyramid_asyncio.aioinspect import is_generator
log = logging.getLogger(__name__)


class TransactionManager(dict):
    _instance = None
    databases = []

    def __getitem__(self, key):
        if key not in self:
            self[key] = orm.Transaction(key)
        return super().__getitem__(key)

    def register_database(self, database):
        self.databases.append(database)

    @asyncio.coroutine
    def on_response(self, response):
        commit = (200 <= response.status_code < 400)

        if commit:
            yield from self.commit()
        else:
            yield from self.rollback()

    @asyncio.coroutine
    def commit(self):
        log.info('Commiting transactions')
        for key, val in self.items():
            try:
                if not val.cursor:
                    continue
                log.info('Commit {}'.format(key))
                yield from val.commit()
            except Exception:
                log.exception('Unexpected exception')

    @asyncio.coroutine
    def rollback(self):
        log.info('Rollbacking transactions')
        for key, val in self.items():
            try:
                if not val.cursor:
                    continue
                log.info('Rollback {}'.format(key))
                yield from val.rollback()
            except Exception:
                log.exception('Unexpected exception')


def tween_factory(handler, registry):

    @asyncio.coroutine
    def tween(request):
        transac = TransactionManager()
        request.set_property(lambda _: transac, 'transaction',
                             reify=True)
        try:
            response = handler(request)
            if is_generator(response):
                response = yield from response
            yield from transac.on_response(response)
        except:  # /!\ rollback event on SystemExit
            yield from transac.rollback()
            raise
        return response

    return tween
