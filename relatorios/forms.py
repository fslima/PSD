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

class FormRelTpMaterial(forms.Form):
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
	tp_material = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), label = 'Tipo de Material')
	formato = forms.ChoiceField([('',''), ('Em Tela','Em Tela'), ('Planilha','Planilha'),], 
				initial = ('',''),
				label = 'Formato')
	
	fields = ('dt_liberacaoP', 'dt_liberacaoA', 'tp_material', 'formato')

class FormRelRequisicao(forms.Form):
	dt_solicitacaoP = forms.DateField(
				label = 'Solicitada a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	dt_solicitacaoA = forms.DateField(
				label = 'Solicitada até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
			)
	centro_custo = forms.ModelChoiceField(queryset = CentroCusto.objects.all().order_by('nome_centro_custo'), required = False, label = 'Centro de Custo')
	item_requisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Requisição')
	status = forms.ChoiceField([('',''), ('Aprovada','Aprovada'), ('Aguardando Aprovação','Aguardando Aprovação'), ('Reprovada','Reprovada'), ('Excluido','Excluido')], 
				initial = ('',''),
				label = 'Situação', required = False)

	formato = forms.ChoiceField([('',''), ('Em Tela','Em Tela'), ('Planilha','Planilha'),], 
				initial = ('',''),
				label = 'Formato')
	
	fields = ('dt_solicitacaoP', 'dt_solicitacaoA', 'centro_custo', 'item_requisicao', 'status', 'formato')

