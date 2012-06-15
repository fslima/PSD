# -* coding:utf-8 -*-

from django import forms
from interno.models import *

class FormRelFornecedorGeral(forms.Form):	
	dt_liberacaoP = forms.DateField(
				label = 'Liberacao a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	dt_liberacaoA = forms.DateField(
				label = 'Liberacao até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	
	fields = ('dt_liberacaoP', 'dt_liberacaoA')

class FormRelFornecedorGrupoMercadoria(forms.Form):	
	dt_liberacaoP = forms.DateField(
				label = 'Liberacao a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	dt_liberacaoA = forms.DateField(
				label = 'Liberacao até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	grupo_mercadoria = forms.ModelChoiceField(queryset = GrupoMercadoria.objects.all().order_by('nome_grupo_mercadoria'), label = 'Grupo de Mercadoria')
	
	fields = ('dt_liberacaoP', 'dt_liberacaoA', 'grupo_mercadoria')

