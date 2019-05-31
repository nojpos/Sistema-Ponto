from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Frequencia, Funcionario, ConfiguracaoHora, TipoPonto, StatusPonto
from .forms import FrequenciaForm, JustificativaForm


@login_required
def home_page(request):
    frequencia = Frequencia.objects.all()
    user = request.user
    func = Funcionario.objects.get(usuario=user)
    return render(request, 'app_ponto/index.html', {'frequencia': frequencia, 'user': user, 'func': func})


@login_required
def lista_frequencia(request):
    frequencia=Frequencia.objects.all()
    user = request.user
    return render(request, 'app_ponto/frequencia.html', {'frequencia': frequencia, 'user': user})


@login_required
def lista_nao_justificados(request):
    user = request.user
    func = Funcionario.objects.get(usuario=user)
    frequencia_inconsistente_nao_justificada = Frequencia.objects.filter(status_ponto=2, juntificativa=None,
                                                                         funcionario=func.id)
    return render(request, 'app_ponto/nao_justificados.html', {'nao_justificada': frequencia_inconsistente_nao_justificada, 'user': user})


@login_required
def relatorio_inconsistentes(request):
    frequencia = Frequencia.objects.all()
    user = request.user
    func = Funcionario.objects.get(usuario=user)
    return render(request, 'app_ponto/relatorio_inconsistentes.html', {'frequencia': frequencia, 'user': user, 'func': func})


#ESSA FUNÇÃO RECEBE A HORA ATUAL E A CONFIGURAÇÃO DE HORA E RETORNA SE A HORA É INCONSISTENRE OU CONSISTENTE
def verificar_hora(hora_atual, config_hora):

    if hora_atual.hour == config_hora.hour:
        if hora_atual.minute >= config_hora.minute + 15:
            inco = StatusPonto.objects.get(id=2)
            return inco
        else:
            con = StatusPonto.objects.get(id=1)
            return con
    elif hora_atual.hour < config_hora.hour:
        con = StatusPonto.objects.get(id=1)
        return con
    else:
        inco = StatusPonto.objects.get(id=2)
        return inco


#Função para testes
@login_required
def teste_registro_ponto(request):

    # Recupera o ID do usuáio autenticado
    user = request.user.id
    print('Usuário', user)

    #Recupera a hora atual
    data_atual = datetime.now()
    print('Data Atual', data_atual.date())

    #Recupera a hora atual
    hora_atual = datetime.now()
    print('Hora Atual', hora_atual.time())


    #Verifica a quantidade de registros da tebela frequencia do dia atual para usuario logado
    qtd = Frequencia.objects.filter(funcionario=user, data_resgistro=data_atual.date()).count()
    #print('Quantidade Id User', qtd)


    #Recupera a instancia do funcionário buscando pelo o usuário logado
    func = Funcionario.objects.get(usuario=user)
    print('Id Funcionario = ', func.id)

    #Verifica a quantidade de registros da tebela frequencia do dia atual para funcionário logado
    qtd_fun = Frequencia.objects.filter(funcionario=func.id, data_resgistro=data_atual.date()).count()
    print('Quantidade Id Funcionário', qtd_fun)

    #IMPRIMIR CONFIGURAÇÃO HORA
    #print('Configuração hora', func.conf_hora.conf_hora_saida_1)
    #print('Configuração hora hora', func.conf_hora.conf_hora_entrada_1.hour)
    #print('Configuração hora minuto', func.conf_hora.conf_hora_entrada_1.minute)
    #print('Configuração hora segundos', func.conf_hora.conf_hora_entrada_1.second)


    #Recupera a instacia do TipoPonto para adicionar no registro da tabela Frequencia.
    entrada = TipoPonto.objects.get(id=1)
    print(entrada)
    saida = TipoPonto.objects.get(id=2)
    print(saida)


    print('Configuração hora', func.conf_hora.conf_hora_entrada_1)
    print('Hora Atual', hora_atual.time())
    print('O ponto é', verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_entrada_1))


    if qtd == 0:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 1:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 2:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 3:
        return HttpResponse('Quantidade = {}'.format(qtd))

    else:
        return HttpResponse('Quantidade = {}'.format(qtd))


#Função de registrar ponto - Produção
@login_required
def registar_ponto(request):
    form = FrequenciaForm()

    #Recupera o ID do usuáio autenticado
    user = request.user.id
    print('Usuário', user)

    #Recupera a hora atual
    hora_atual = datetime.now()
    print('Hora atual', hora_atual.time())

    #Recupera a data atual
    data_atual = datetime.now()
    print('Data atual', data_atual.date())

    #Recupera a instancia do funcionário buscando pelo o usuário logado
    func = Funcionario.objects.get(usuario=user)
    print('Id Funcionario = ', func.id)

    #Verifica a quantidade de registros da tebela frequencia do dia atual para funcionário logado
    qtd_fun = Frequencia.objects.filter(funcionario=func.id, data_resgistro=data_atual.date()).count()
    print('Quantidade Id Funcionário', qtd_fun)

    #Recupera a instacia do TipoPonto para adicionar no registro da tabela Frequencia.
    entrada = TipoPonto.objects.get(id=1)
    print(entrada)
    saida = TipoPonto.objects.get(id=2)
    print(saida)


    #Verifica se é uma requisição do tipo POST
    if request.method == "POST":
        form = FrequenciaForm(request.POST)

        #Verifica se o formulário é válido
        if form.is_valid():
            post = form.save(commit=False)

            #Esses condicionais verificam a quantidade de registros que existem na frequencia para poder adicionar um novo registro
            if qtd_fun == 0:
                if func.conf_hora.conf_hora_entrada_1 != None:
                    post.hora_ponto = hora_atual.time()
                    post.funcionario = func
                    post.tipo_ponto = entrada
                    post.status_ponto = verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_entrada_1)
                    post.save()
                else:
                    return render(request, 'app_ponto/erro_qtd_maxima_ponto.html', {'func': func})

            elif qtd_fun == 1:
                if func.conf_hora.conf_hora_saida_1 != None:
                    post.hora_ponto = hora_atual.time()
                    post.funcionario = func
                    post.tipo_ponto = saida
                    post.status_ponto = verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_saida_1)
                    post.save()
                else:
                    return render(request, 'app_ponto/erro_qtd_maxima_ponto.html', {'func': func})

            elif qtd_fun == 2:
                if func.conf_hora.conf_hora_entrada_2 != None:
                    post.hora_ponto = hora_atual.time()
                    post.funcionario = func
                    post.tipo_ponto = entrada
                    post.status_ponto = verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_entrada_2)
                    post.save()
                else:
                    return render(request, 'app_ponto/erro_qtd_maxima_ponto.html', {'func': func})

            elif qtd_fun == 3:
                if func.conf_hora.conf_hora_saida_2 != None:
                    post.hora_ponto = hora_atual.time()
                    post.funcionario = func
                    post.tipo_ponto = saida
                    post.status_ponto = verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_saida_2)
                    post.save()
                else:
                    return render(request, 'app_ponto/erro_qtd_maxima_ponto.html', {'func': func})

            else:
                return render(request, 'app_ponto/erro_qtd_maxima_ponto.html', {'func': func})

            return redirect('registar_ponto')

        else:
            form = FrequenciaForm()

    return render(request, 'app_ponto/registro_ponto.html', {'form': form, 'qtd_fun': qtd_fun, 'func': func})


@login_required
def justificar_inconsistente(request, frequencia_id):
    frequencia = Frequencia.objects.get(pk=frequencia_id)
    form = JustificativaForm(request.POST or None, instance=frequencia)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('frequencia')
    else:
        return render(request, 'app_ponto/justificar_ponto.html', {'form': form, 'frequencia': frequencia})


@login_required
def relatorio(request):
    user = request.user
    func = Funcionario.objects.get(usuario=user)
    funcionario = Funcionario.objects.filter(lider=func.id)
    return render(request, 'app_ponto/relatorio.html', {'funcionario': funcionario, 'user': user, 'func': func})


@login_required
def relatorio_pontos_inconsistentes(request, funcionario_id):
    frequencia_inconsistente = Frequencia.objects.filter(funcionario=funcionario_id, status_ponto=2)
    func = Funcionario.objects.get(pk=funcionario_id)
    return render(request, 'app_ponto/relatorio_pontos_inconsistentes.html', {'frequencia_inconsistente': frequencia_inconsistente, 'func': func})