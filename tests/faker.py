from functools import cache
from faker.providers import BaseProvider
from lbrc_flask.pytest.faker import FakeCreator, FakeCreatorArgs
from coloprevent.model import Pack, PackShipment, PackType, Site


class SiteFakeCreator(FakeCreator):
    cls = Site

    def _create_item(self, save: bool, args: FakeCreatorArgs):
        result = self.cls(
            site_name = args.get('site_name', self.faker.unique.company()),
            site_backup_contact = args.get('site_backup_contact', self.faker.unique.name()),
            site_primary_contact = args.get('site_primary_contact', self.faker.unique.name()),
            site_code = args.get('site_code', self.faker.unique.pystr()),
        )

        return result


class PackTypeFakeCreator(FakeCreator):
    cls = PackType

    def _create_item(self, save: bool, args: FakeCreatorArgs):
        packname = args.get('packtype_name', self.faker.unique.word())
        result = self.cls(
            packtype_name = packname,
        )

        return result


class PackShipmentFakeCreator(FakeCreator):
    cls = PackShipment

    def _create_item(self, save: bool, args: FakeCreatorArgs):
        result = self.cls(
            date_posted = args.get('date_posted', self.faker.date_object()),
            date_received = args.get('date_received'),
            next_due = args.get('next_due'),
            site = args.get('site', self.faker.site().get()),
        )

        return result


class PackFakeCreator(FakeCreator):
    cls = Pack

    def _create_item(self, save: bool, args: FakeCreatorArgs):
        result = self.cls(
            pack_identity = args.get('pack_identity', self.faker.unique.random_int()),
            pack_expiry = args.get('pack_expiry', self.faker.date_object()),
            packtype = args.get('packtype', self.faker.packtype().get()),
            pack_shipment = args.get('pack_shipment', self.faker.pack_shipment().get()),
            pack_action = args.get('pack_action', self.faker.sentence(nb_words=6)),
        )

        return result


class ColoPreventProvider(BaseProvider):
    @cache
    def pack(self):
        return PackFakeCreator(self)

    @cache
    def site(self):
        return SiteFakeCreator(self)

    @cache
    def pack_shipment(self):
        return PackShipmentFakeCreator(self)

    @cache
    def packtype(self):
        return PackTypeFakeCreator(self)
