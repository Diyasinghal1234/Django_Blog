from django.urls import path
from . import views
urlpatterns = [
    #path('',views.test),
    path('loginn/',views.loginn,name='login-page'),
    path('',views.signup),
    path('home/',views.home),
    path('MyPosts/',views.MyPosts,name='myposts'),
    path('newpost/',views.newpost),
    path('signout/',views.signout),
    path('editpost/<int:post_id>/', views.editpost, name='editpost'),
    path('deletepost/<int:post_id>/', views.deletepost, name='deletepost'),
    path('deleteimage/<int:image_id>/', views.delete_image, name='deleteimage'),
    path('add-comment/<int:post_id>/',views.add_comment,name='add_comment'),
    path('delete-comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),
    path('edit-comment/<int:comment_id>/',views.edit_comment,name='edit_comment'),
    path('react/<int:post_id>/<str:reaction_type>/',views.react_post,name='react_post'),
]