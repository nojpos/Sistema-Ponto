from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Frequencia, Funcionario, ConfiguracaoHora, TipoPonto, StatusPonto
from .forms import FrequenciaForm


@login_required
def home_page(request):
    return render(request, 'app_ponto/index.html')


@login_required
def lista_frequencia(request):
    frequencia=Frequencia.objects.all()
    return render(request, 'app_ponto/frequencia.html', {'frequencia': frequencia})


#ESSA FUNÇÃO RECEBE A HORA ATUAL E A CONFIGURAÇÃO DE HORA E RETORNA SE A HORA É INCONSISTENRE OU CONSISTENTE (Falta validar se já passaram 15 min
#da hora configurada)
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


    print('Configuração hora', func.conf_hora.conf_hora_entrada_2)
    print('Hora Atual', hora_atual.time())
    print('O ponto é', verificar_hora(hora_atual.time(), func.conf_hora.conf_hora_entrada_2))


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


'''
class RegitrarForm(FormView):
    template_name = 'app_ponto/registrar.html'
    form_class = RegistroPontoForm

    def form_valid(self, form):
        hora_atual = datetime.now()
        print(hora_atual.time())
        dados = form.clean()
        s = Frequencia(juntificativa=dados['juntificativa'], )
        s.hora_entrada_2=hora_atual.time()
        s.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('frequencia')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'app_ponto/name.html', {'form': form})


def funcionario_new(request):
    form = FuncionarioForm()

    if request.method == "POST":
        form = FuncionarioForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('frequencia')

    else:
        form = FuncionarioForm()

    return render(request, 'app_ponto/registro_ponto.html', {'form': form})
'''


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
                post.hora_ponto = hora_atual.time()
                post.funcionario = func
                post.tipo_ponto = entrada
                post.save()

            elif qtd_fun == 1:
                post.hora_ponto = hora_atual.time()
                post.funcionario = func
                post.tipo_ponto = saida
                post.save()

            elif qtd_fun == 2:
                post.hora_ponto = hora_atual.time()
                post.funcionario = func
                post.tipo_ponto = entrada
                post.save()

            elif qtd_fun == 3:
                post.hora_ponto = hora_atual.time()
                post.funcionario = func
                post.tipo_ponto = saida
                post.save()

            else:
                return HttpResponse('O funcionário {} já registrou o ponto 4 vezes'.format(func))

            return redirect('frequencia')

        else:
            form = FrequenciaForm()

    return render(request, 'app_ponto/registro_ponto.html', {'form': form})