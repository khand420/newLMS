from django.urls import path
from .views import AuthView, SignupView
from . import views, viewsUser
from django.views.generic import RedirectView


urlpatterns = [
    # path('industrylist', views.industrylist, name = 'industrylist'),
    # path('', views.login_request, name = 'login'),
    path("auth/login/", views.login_request, name="login"),
    # path('logout/', RedirectView.as_view(url = '/login')),
    # path('auth/signup/', views.signup, name='signup'), # newly added
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # path("auth/login/", views.login_request, {'template_name': 'auth_login.html'}, name="login"),
    # path('auth/signup/', views.signup, {'template_name': 'auth_register.html'}, name='signup'),


    # path("auth/login/", AuthView.as_view(), name="login"),
    # path('auth/signup/', AuthView.as_view(), name='signup'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', AuthView.as_view(), name='activate'),

    # path(
    #     "auth/login/",
    #     AuthView.as_view(template_name="auth_login_basic.html"),
    #     name="auth-login-basic",
    # ),
    # path(
    #     "auth/register/",
    #     AuthView.as_view(template_name="auth_register_basic.html"),
    #     name="auth-register-basic",
    # ),
    path(
        "auth/forgot_password/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password",
    ),


    path('departments', viewsUser.departments, name = 'departments'),
    path('department_add/', viewsUser.department_add, name='department_add'),
    path('department_update/<int:id>', viewsUser.department_update, name='department_update'),
    path('department_delete/<int:id>', viewsUser.department_delete, name='department_delete'),

    path('clients', viewsUser.clients, name = 'clients'),
    path('client_add/', viewsUser.client_add, name='client_add'),
    path('client_update/<int:id>', viewsUser.client_update, name='client_update'),
    # path('telecaller/', viewsUser.telecallers, name='telecallers'),

    path('clients-user-list', viewsUser.telecaller_list, name = 'clients-user'),
    path('clients-user/add/', viewsUser.telecaller_add, name='clients-user-create'),
    path('clients-user/update/<int:id>/', viewsUser.telecaller_update, name='clients-user-update'),
    path('clients-user/delete/<int:id>/', viewsUser.telecaller_delete, name='clients-user-delete'),


]
