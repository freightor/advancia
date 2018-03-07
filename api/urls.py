from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path("",views.tester,name="tester"),
    path("transact/",views.run_transaction,name="transact"),
]