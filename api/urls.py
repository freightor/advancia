from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path("transact/",views.run_transaction,name="transact"),
    path("transact/verify/",views.verify_transaction,name="verify"),
    path("transact/resend/",views.resend_code,name="resend")
]