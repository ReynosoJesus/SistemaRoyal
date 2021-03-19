from django.conf.urls import url 
from sistema import views





#https://bezkoder.com/django-react-axios-rest-framework/#Create_Serializer_class_for_Data_Model 
urlpatterns = [ 
    url(r'^api/getCertificados/(?P<pk>[0-9]+)$', views.certificados_list),
    url(r'^api/alumno$', views.alumno_list), #/api/tutorials: GET, POST, DELETE
    url(r'^api/alumno/(?P<pk>[0-9]+)$', views.alumno_detail),#/api/tutorials/:id: GET, PUT, DELETE
    url(r'^api/grupo/(?P<pk>[0-9]+)$', views.grupos_detail),#/api/tutorials/published: GET
    url(r'^api/libros$', views.libros_detail), #/api/tutorials: GET, POST, DELETE
]