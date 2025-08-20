
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/male/', views.male_profiles, name='male_profiles'),
    path('profiles/female/', views.female_profiles, name='female_profiles'),
    path("profiles/<int:pk>/<slug:slug>/", views.profile_detail, name="profile_detail"),
    path('api/subcastes/<int:caste_id>/', views.subcastes_api, name='subcastes_api'),
    path("services/<int:pk>/", views.service_detail, name="service_detail"),
    path("search/", views.profile_search, name="profile_search"),
]