from django.urls import include, path
from rest_framework import routers
from . import views
from .views import Transactions, Statement, Debits, Account, Credits
router = routers.DefaultRouter()
router.register(r'monoid', views.MonoIdViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('transactions/', Transactions.as_view()),
    path('statement/', Statement.as_view()),
    path('debit/', Debits.as_view()),
    path('credit/', Credits.as_view()),
    path('account/', Account.as_view()),
]