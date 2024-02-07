from .views import get_user_info, User_create, user_login, user_logout, Todo_create, Get_user_todos, delete_todo, todo_completed
from django.urls import path

urlpatterns = [
    # todo routes
    path('todos/', Todo_create, name='create-todo'),
    path('todos/<int:pk>', Get_user_todos, name='get-user-todos'),
    path('todos/delete/<int:pk>', delete_todo, name='delete-todo'),
    path('todos/completed/<int:pk>', todo_completed, name='todo-completed'),

    # user routes
    path('users/', get_user_info, name='get-user'),
    path('users/create', User_create, name='create-user'),
    path('users/login', user_login, name='login-user'),
    path('users/logout', user_logout, name='logout-user'),
]