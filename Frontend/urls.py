from django.urls import path
from Frontend import views
from Frontend.views import PostModalView
from Frontend.models import Post

urlpatterns = [
    # User creation, login and logout
    path('user/register/',views.BlogUserCreateView.as_view()),
    path('user/login/',views.LoginView.as_view()),
    path('user/logout/',views.LogoutView.as_view()),
    # User update
    path('user/',views.BlogUSerRetrieveUpdateView.as_view()),
    # Post creation, view, update and delete 
    path('post/',views.PostCreateView.as_view()),
    path('post/<int:id>/',views.PostRetreiveUpdateDestroyView.as_view()),
    # Post list view for user and for all
    path('post/user/',views.UserPostListView.as_view()),
    path('post/public/',views.PostListView.as_view()),
]
