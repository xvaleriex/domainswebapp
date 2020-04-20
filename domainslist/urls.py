from django.urls import path
from . import views

urlpatterns = [
	path('', views.domainslist_index, name='domainslist_index'),
	path("<int:id>/", views.domain_detail, name="domain_detail"),
]
