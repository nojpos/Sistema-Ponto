from django.urls import path
from .views import lista_frequencia, teste_registro_ponto, registar_ponto,home_page
from django.views.generic import RedirectView

urlpatterns = [
    path('frequencia/', lista_frequencia, name='frequencia'),
    path('', home_page, name='home'),
    path('teste/ponto', teste_registro_ponto, name='teste_ponto'),
    path('registrar/ponto', registar_ponto, name='registar_ponto'),

]