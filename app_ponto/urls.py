from django.urls import path
from .views import lista_frequencia, teste_registro_ponto, registar_ponto,home_page, justificar_inconsistente, relatorio_inconsistentes, lista_nao_justificados, relatorio, relatorio_pontos_inconsistentes
from django.views.generic import RedirectView

urlpatterns = [
    path('frequencia/', lista_frequencia, name='frequencia'),
    path('home/', home_page, name='home'),
    path('teste/ponto/', teste_registro_ponto, name='teste_ponto'),
    path('', RedirectView.as_view(url='registrar/ponto/')),
    path('registrar/ponto/', registar_ponto, name='registar_ponto'),
    path('frequencia/justificar/<int:frequencia_id>/', justificar_inconsistente, name='justificar'),
    path('nao/justificados/justificar/<int:frequencia_id>/', justificar_inconsistente, name='justificar_nao_justificados'),
    #path('relatorio/', relatorio_inconsistentes, name='relatorio'),
    path('relatorio/', relatorio, name='relatorio'),
    path('relatorio/relatorio/inconsistentes/<int:funcionario_id>/', relatorio_pontos_inconsistentes, name='relatorio_inconsistentes'),
    path('nao/justificados/', lista_nao_justificados, name='nao_justificados'),
]