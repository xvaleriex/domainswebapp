from django_extensions.management.jobs import DailyJob
from domainslist.models import Domain, DomainFlag
from datetime import datetime, timedelta
from dateutil import tz

class Job(DailyJob):
    help = "Job that sets EXPIRED flag to all expired domains"

    def execute(self):
        today = datetime.utcnow().date()
        start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
        end = start + timedelta(1)
        expired_domains = Domain.objects.filter(datetime_expiration__range=(start, end))
        for d in expired_domains:
            expired_flag = DomainFlag(domain=d, type='EXPIRED', datetime_from=today, datetime_to=None)
            expired_flag.save()
