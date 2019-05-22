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

@login_required
def teste_registro_ponto(request):

    user = request.user.id
    print('Usuário', user)

    data_atual = datetime.now()
    print('Data Atual', data_atual.date())

    hora_atual = datetime.now()
    print('Hora Atual', hora_atual.time())


    qtd = Frequencia.objects.filter(funcionario=user, data_resgistro=data_atual.date()).count()
    print('Quantidade Id User', qtd)


    func = Funcionario.objects.get(usuario=user)
    print('Id Funcionario = ', func.id)

    qtd_fun = Frequencia.objects.filter(funcionario=func.id, data_resgistro=data_atual.date()).count()
    print('Quantidade Id Funcionário', qtd_fun)

    #IMPRIMIR CONFIGURAÇÃO HORA
    print(func.conf_hora.conf_hora_entrada_1)


    entrada = TipoPonto.objects.get(id=1)
    print(entrada)
    saida = TipoPonto.objects.get(id=2)
    print(saida)

    if hora_atual.time() > func.conf_hora.conf_hora_entrada_1:
        inco = StatusPonto.objects.get(id=2)
        print('Hora maior = ', inco)
    else:
        con = StatusPonto.objects.get(id=1)
        print('Hora maior = ', con)


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


@login_required
def registar_ponto(request):
    form = FrequenciaForm()

    user = request.user.id
    print('Usuário', user)

    hora_atual = datetime.now()
    print('Hora atual', hora_atual.time())

    data_atual = datetime.now()
    print('Data atual', data_atual.date())

    func = Funcionario.objects.get(usuario=user)
    print('Id Funcionario = ', func.id)

    qtd_fun = Frequencia.objects.filter(funcionario=func.id, data_resgistro=data_atual.date()).count()
    print('Quantidade Id Funcionário', qtd_fun)

    entrada = TipoPonto.objects.get(id=1)
    print(entrada)
    saida = TipoPonto.objects.get(id=2)
    print(saida)


    if request.method == "POST":
        form = FrequenciaForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

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