from django.urls import path
from .views import lista_frequencia, teste_registro_ponto, registar_ponto
from django.views.generic import RedirectView

urlpatterns = [
    path('frequencia/', lista_frequencia, name='frequencia'),
    path('', RedirectView.as_view(url='frequencia')),
    path('teste/ponto', teste_registro_ponto, name='teste_ponto'),
    path('registrar/ponto', registar_ponto, name='registar_ponto'),

]
