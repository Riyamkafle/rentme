
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('login/',views.signin,name = "login"),
    path('register/',views.register,name = "register"),
    path('property/<int:id>/',views.propertyDetail,name = "propertyDetail" ),
    path('contactOwner/',views.contact_owner,name ="contactOwner" ),
    path('messages/',views.messages,name = "messages"),
    path('message/<int:pk>',views.messageDetail,name = "messageDetail"),
    path('logout/', views.logout_view, name='logout'),
    path('properties/new/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_update, name='property_update'),



]
