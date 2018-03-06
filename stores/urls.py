from django.urls import path
from stores import views
app_name = "stores"
urlpatterns = [
    path("transactions/",views.transaction_list,name="trans_list"),
    path("transactions/<int:pk>/", views.transaction_detail, name="trans_detail")
]