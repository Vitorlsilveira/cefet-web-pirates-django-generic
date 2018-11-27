from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tesouro
# Create your views here.
class ListarTesouros(LoginRequiredMixin,ListView):
    model = Tesouro
    template_name = "lista_tesouros.html"

    def get_queryset(self, **kwargs):
        return Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = 0
        for tesouro in context['object_list']:
            context['total_geral'] += tesouro.valor_total
        return context

class RemoverTesouro(LoginRequiredMixin,DeleteView):
    model = Tesouro
    success_url = reverse_lazy('lista_tesouros')

class SalvarTesouro(LoginRequiredMixin):
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = "salvar_tesouro.html"
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(SalvarTesouro,CreateView):
    pass

class AtualizarTesouro(SalvarTesouro,UpdateView):
    pass