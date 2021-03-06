import uuid
from datetime import date

import marshmallow as ma

from app.utility.base_object import BaseObject
from app.objects.interfaces.i_object import FirstClassObjectInterface
from plugins.pathfinder.app.objects.secondclass.c_host import HostSchema


class ReportSchema(ma.Schema):

    id = ma.fields.String(missing=None)
    name = ma.fields.String()
    hosts = ma.fields.Dict(keys=ma.fields.String(), values=ma.fields.Nested(HostSchema()))
    scope = ma.fields.String()
    network_map = ma.fields.Dict(keys=ma.fields.String(), values=ma.fields.List(ma.fields.String()))

    @ma.post_load()
    def build_report(self, data, **_):
        return VulnerabilityReport(**data)


class VulnerabilityReport(FirstClassObjectInterface, BaseObject):

    schema = ReportSchema()

    @property
    def unique(self):
        return self.hash('%s' % self.id)

    def __init__(self, id=None, name=None, hosts=None, scope=None, **kwargs):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.name = name if name else 'vulnerability-report-%s' % date.today().strftime("%b-%d-%Y")
        self.hosts = hosts or dict()
        self.scope = scope
        self.network_map = None

    def store(self, ram):
        existing = self.retrieve(ram['vulnerabilityreports'], self.unique)
        if not existing:
            ram['vulnerabilityreports'].append(self)
            return self.retrieve(ram['vulnerabilityreports'], self.unique)
        existing.update('name', self.name)
        existing.update('hosts', self.hosts)
        existing.update('network_map', self.network_map)
        return existing
