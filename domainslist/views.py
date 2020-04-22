from django.shortcuts import render
from domainslist.models import Domain, DomainFlag
from datetime import datetime


def domainslist_index(request):
    not_deleted_domains = Domain.objects.filter(datetime_deletion__isnull=True)
    context = {
        'domains': not_deleted_domains
    }
    return render(request, 'domainslist_index.html', context)


def domain_detail(request, id):
    domain = Domain.objects.get(pk=id)
    context = {
        'domain': domain
    }
    return render(request, 'domain_detail.html', context)
