from django.test import TestCase
from domainslist.models import Domain, DomainFlag
from datetime import datetime
from django.utils import timezone
from django.urls import reverse


# models test
class DomainsListTest(TestCase):
    # datetime_deletion=datetime.fromisoformat("2020-01-01T12:12:00+00:00")
    def create_domain(
        self,
        fqdn="testfqdn",
        datetime_creation=datetime.fromisoformat("2019-12-10T12:10:23+00:00"),
        datetime_expiration=datetime.fromisoformat("2020-07-05T12:12:00+00:00"),
        datetime_deletion=None,
    ):
        if datetime_deletion is None:
            return Domain.objects.create(
                fqdn=str(fqdn),
                datetime_creation=str(datetime_creation),
                datetime_expiration=str(datetime_expiration),
                datetime_deletion=None,
            )
        else:
            return Domain.objects.create(
                fqdn=str(fqdn),
                datetime_creation=str(datetime_creation),
                datetime_expiration=str(datetime_expiration),
                datetime_deletion=str(datetime_deletion),
            )

    def create_domain_flag(
        self,
        domain,
        type="EXPIRED",
        datetime_from=datetime.fromisoformat("2020-01-01T12:12:05+00:00"),
        datetime_to=datetime.fromisoformat("2021-07-05T12:12:00+00:00"),
    ):
        self.domain = domain
        return DomainFlag.objects.create(
            domain=domain,
            type=type,
            datetime_from=datetime_from,
            datetime_to=datetime_to,
        )

    # Models test
    def test_domainflag_is_active(self):
        d1 = self.create_domain()
        f1 = self.create_domain_flag(d1)
        # Test type of created objects
        self.assertTrue(isinstance(d1, Domain))
        self.assertTrue(isinstance(f1, DomainFlag))
        # Test that flag is active
        self.assertEqual(f1.is_active(), True)

    # Views tests
    def test_domainslist_index_view_statuscode(self):
        # Test status code
        d1 = self.create_domain()
        d2 = self.create_domain(
            fqdn="testfqdn2",
            datetime_creation=datetime.fromisoformat("2019-11-10T12:10:23+00:00"),
            datetime_expiration=datetime.fromisoformat("2020-04-05T12:12:00+00:00"),
        )
        resp = self.client.get("/domainslist/")
        self.assertEqual(resp.status_code, 200)

    def test_domainslist_index_view_active_domains(self):
        # Test that that domains that are active(datetime_deletion is Null))are displayed
        d1 = self.create_domain()
        d2 = self.create_domain(
            fqdn="testfqdn2",
            datetime_creation=datetime.fromisoformat("2019-11-10T12:10:23+00:00"),
            datetime_expiration=datetime.fromisoformat("2020-04-05T12:12:00+00:00"),
        )
        resp = self.client.get("/domainslist/")
        domains_count = len(resp.context["domains"])
        self.assertEqual(domains_count, 2)

        # Test domains attributes
        test_d1 = resp.context["domains"][0]
        self.assertEqual(test_d1.id, d1.id)
        self.assertEqual(str(test_d1.datetime_creation), d1.datetime_creation)
        self.assertEqual(str(test_d1.datetime_expiration), d1.datetime_expiration)

        test_d2 = resp.context["domains"][1]
        self.assertEqual(test_d2.id, d2.id)
        self.assertEqual(str(test_d2.datetime_creation), d2.datetime_creation)
        self.assertEqual(str(test_d2.datetime_expiration), d2.datetime_expiration)

    def test_domainslist_index_view_not_active(self):
        # Test that that domains that are NOT active are not displayed
        d3 = self.create_domain(
            fqdn="testfqdn3",
            datetime_creation=datetime.fromisoformat("2019-11-10T12:10:23+00:00"),
            datetime_expiration=datetime.fromisoformat("2020-04-05T12:12:00+00:00"),
            datetime_deletion=datetime.fromisoformat("2020-01-01T12:12:00+00:00"),
        )
        d4 = self.create_domain(
            fqdn="testfqdn4",
            datetime_creation=datetime.fromisoformat("2019-11-10T12:10:23+00:00"),
            datetime_expiration=datetime.fromisoformat("2020-04-05T12:12:00+00:00"),
            datetime_deletion=datetime.fromisoformat("2020-01-01T12:12:00+00:00"),
        )
        resp = self.client.get("/domainslist/")
        domains_count = len(resp.context["domains"])
        self.assertEqual(domains_count, 0)

    def test_domainslist_detail_view(self):
        # Create test Domain and DomainFlag objects
        d1 = self.create_domain()
        f1 = self.create_domain_flag(d1)

        # First, test response status code
        resp = self.client.get("/domainslist/1/")
        self.assertEqual(resp.status_code, 200)

        # Then test that domain in response content indeed matched our test domain
        # and matching attributes
        content_d = resp.context["domain"]
        self.assertEqual(content_d.id, d1.id)
        self.assertEqual(str(content_d.datetime_creation), d1.datetime_creation)
        self.assertEqual(str(content_d.datetime_expiration), d1.datetime_expiration)

        # Same test attributes for domain flag
        content_f = resp.context["domain"].domainflag_set.all()[0]
        self.assertEqual(content_f.id, f1.id)
        self.assertEqual(content_f.type, f1.type)
        self.assertEqual(str(content_f.datetime_from), str(f1.datetime_from))
        self.assertEqual(str(content_f.datetime_to), str(f1.datetime_to))
