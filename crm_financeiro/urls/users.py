from django.urls import path
from crm_financeiro.views.users import (
    RegisterUserView,
    UserFormActionRouter,
    ListUsers,
    UsersCSVExportView,
    DetailUser,
    UpdateUser,
    DeleteUser,
    ChangePasswordView
)

urlpatterns = [
    path('register_user/', RegisterUserView.as_view(), name='register_user'),
    path('user-action-router/', UserFormActionRouter.as_view(), name='user_action_router'),
    path('listar-usuarios/', ListUsers.as_view(), name='list_users'),
    path('export-users/', UsersCSVExportView.as_view(), name='export_users'),
    path('detalhes-usuario/<str:username>/', DetailUser.as_view(), name='detail_user'),
    path('atualizar-usuario/<str:username>/', UpdateUser.as_view(), name='update_user'),
    path('delete-user/<str:username>/', DeleteUser.as_view(), name='delete_user'),
    path('trocar-senha/', ChangePasswordView.as_view(), name='change_user_password')
]
