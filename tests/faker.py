from faker.providers import BaseProvider
from lbrc_flask.pytest.faker import FakeCreator
from coloprevent.model import Pack, PackShipment, PackType, Site
from functools import cache


class SiteFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(Site)

    def get(self, **kwargs):
        result = self.cls(
            site_name = kwargs.get('site_name') or self.faker.unique.word(),
            site_backup_contact = kwargs.get('site_backup_contact') or self.faker.unique.name(),
            site_primary_contact = kwargs.get('site_primary_contact') or self.faker.unique.name(),
            site_code = kwargs.get('site_code') or self.faker.unique.pystr(),
        )

        return result


class SiteProvider(BaseProvider):
    @cache
    def site(self):
        return SiteFakeCreator()


class PackTypeFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(PackType)

    def get(self, **kwargs):
        result = self.cls(
            packtype_name = kwargs.get('packtype_name') or self.faker.unique.word(),
        )

        return result


class PackTypeProvider(BaseProvider):
    @cache
    def packtype(self):
        return PackTypeFakeCreator()


class PackShipmentFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(PackShipment)
        self.faker.add_provider(SiteProvider)

    def get(self, **kwargs):
        result = self.cls(
            date_posted = kwargs.get('date_posted') or self.faker.date_object(),
            date_received = kwargs.get('date_received'),
            next_due = kwargs.get('next_due'),
            site = self.faker.site().get_value_or_get(kwargs, 'site'),
        )

        return result


class PackShipmentProvider(BaseProvider):
    @cache
    def pack_shipment(self):
        return PackShipmentFakeCreator()


class PackFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(Pack)
        self.faker.add_provider(SiteProvider)
        self.faker.add_provider(PackTypeProvider)
        self.faker.add_provider(PackShipmentProvider)

    def get(self, **kwargs):
        result = self.cls(
            pack_identity = kwargs.get('pack_identity') or self.faker.unique.random_int(),
            pack_expiry = kwargs.get('pack_expiry') or self.faker.date_object(),
            packtype = self.faker.packtype().get_value_or_get(kwargs, 'packtype'),
            pack_shipment = self.faker.pack_shipment().get_value_or_get(kwargs, 'pack_shipment'),
            pack_action = kwargs.get('pack_action', self.faker.sentence(nb_words=6)),
        )

        return result


class PackProvider(BaseProvider):
    @cache
    def pack(self):
        return PackFakeCreator()
