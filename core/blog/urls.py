from django.urls import path, include
from .views import *



app_name = "blog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("redirect/", RedirectToUi.as_view(), name="redirct"),
    path("blog/", PostView.as_view(), name="post"),
    path("blog/<int:pk>", PostDetailView.as_view(), name="detail"),
    path("contact/", PostFormView.as_view(), name="contact-form"),
    path("update/<int:pk>", PostUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="delete"),
    path("api/v1/", include("blog.api.v1.urls")),
    path('test/',test,name='test'),

]
