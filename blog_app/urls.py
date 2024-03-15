from django.urls import path, include # added include
from .views import BlogView, PublicView

urlpatterns = [
 path('blog/', BlogView.as_view()),
 path('home/', PublicView.as_view())
]
