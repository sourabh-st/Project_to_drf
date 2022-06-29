
from django.contrib import admin
from django.urls import path, re_path
from social import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('getprofile/',views.ProfileGet.as_view()),
    path('createpost/',views.MyPostCreate.as_view()),
    path('postlist/',views.MyPostList.as_view()),
    path('connections/',views.Connections.as_view()),
    path('follow/',views.Follow.as_view()),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
    
    
    # path('connections/',views.HomeView.as_view())
    
]
