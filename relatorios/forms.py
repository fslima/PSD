# -* coding:utf-8 -*-

from django import forms
from interno.models import *

class FormRelGeral(forms.Form):	
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
	formato = forms.ChoiceField([('',''), ('Em Tela','Em Tela'), ('Planilha','Planilha'),], 
				initial = ('',''),
				label = 'Formato')

	
	fields = ('dt_liberacaoP', 'dt_liberacaoA', 'formato')

class FormRelGrupoMercadoria(forms.Form):	
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
	formato = forms.ChoiceField([('',''), ('Em Tela','Em Tela'), ('Planilha','Planilha'),], 
				initial = ('',''),
				label = 'Formato')
	
	fields = ('dt_liberacaoP', 'dt_liberacaoA', 'grupo_mercadoria', 'formato')

