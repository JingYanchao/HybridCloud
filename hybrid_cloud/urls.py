from django.conf.urls import url
import views
import hybrid_cloud.action.jsonAction as jsonaction

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/',views.login),
    url(r'^index/', views.index),
    url(r'^overview/', views.overview),
    url(r'^instance/', views.instance),
    url(r'^create/', views.create),
    url(r'^action/loginAction/',jsonaction.loginAction),
    url(r'^action/logoutAction/',jsonaction.logoutAction),
    url(r'^action/overviewAction/',jsonaction.overviewAction),
    url(r'^action/instanceActionsAction/',jsonaction.instanceActionsAction),
    url(r'^action/createAdvanceAction/',jsonaction.createAdvanceAction),
    url(r'^action/AliyunActionsAction/', jsonaction.AliyunActionsAction),

]