from django.urls import path
from stores import views
app_name = "stores"
urlpatterns = [
    path("",views.dashboard, name="dashboard"),
    path("transactions/",views.transaction_list,name="trans_list"),
    path("transactions/<int:pk>/", views.transaction_detail, name="trans_detail"),
    path("add/", views.new_store, name="new_store")
]