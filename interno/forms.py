# -* coding:utf-8 -*-

from django import forms
from models import *

class FormGrupoMercadoria(forms.ModelForm):
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nomeGrupoMercadoria',)

class FormUnidadeMaterial(forms.ModelForm):
	
	class Meta:
		model = UnidadeMaterial
		fields = ('nomeUnidadeMaterial',)

class FormCentroCusto(forms.ModelForm):
	
	class Meta:
		model = CentroCusto
		fields = ('nomeCentroCusto', 'gerente')

class FormFabricante(forms.ModelForm):
	
	class Meta:
		model = Fabricante
		fields = ('nomeFabricante',)

class FormMaterial(forms.ModelForm):
	
	fabricante = forms.ModelChoiceField(queryset = Fabricante.objects.all(), label = 'Fabricante')
	tpMaterial = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'))

	class Meta:
		model = Material
		fields = ('nomeMaterial', 'fabricante', 'grupoMercadoria', 'unidadeMaterial', 'tpMaterial')

class FormFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	grupoFornecedor = Group.objects.filter(name = 'fornecedor')
	usuario =  forms.ModelChoiceField(queryset = User.objects.filter(groups__in = grupoFornecedor), label = 'Login no Sistema')
	tel1 = forms.CharField(min_length = 10, max_length = 10)
	tel2 = forms.CharField(min_length = 10, max_length = 10)
	nrimovel = forms.IntegerField(label = 'Nº')
	complemento = forms.CharField(max_length = 50, required = False)
	uf = forms.ChoiceField([('',''), ('AC','AC'), ('AL','AL'), ('AM','AM'),
				('AP','AP'),('BA','BA'), ('CE','CE'), ('DF','DF'),
				('ES','ES'),('GO','GO'), ('MA','MA'), ('MG','MG'),
				('MS','MS'),('MT','MT'), ('PA','PA'), ('PB','PB'),
				('PI','PI'),('PI','PI'), ('PR','PR'), ('RJ','RJ'),
				('RN','RN'),('RO','RO'), ('RR','RR'), ('RS','RS'),
				('SC','SC'),('SE','SE'),('SP','SP'), ('TO','TO')], 
				initial = ('',''),
				label = 'Estado')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'tel1', 'tel2', 'email', 'site', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep')

class FormGruposFornecedor(forms.ModelForm):

	class Meta:
		model = Fornecedor
		fields = ('grupoMercadoria',)

class FormRequisicao(forms.ModelForm):
	
	class Meta:
		model = Requisicao
		fields = ('centroCusto', 'diasParaCotacao')

class FormItemRequisicao(forms.ModelForm):
	
	class Meta:
		model = ItemRequisicao
		fields = ('material', 'qtd')

class FormCotacao(forms.ModelForm):
	
	class Meta:
		model = Cotacao
		fields = ('vlCotacao', 'obs')

class FormMapaComparativo(forms.ModelForm):

	class Meta:
		model = MapaComparativo
		fields = ('obs',)


class FormFiltraMaterial(forms.Form):
	
	nome = forms.CharField(required = False)
	fabricante = forms.ModelChoiceField(queryset=Fabricante.objects.all(), required = False, label = 'Fabricante')
	grupoMercadoria = forms.ModelChoiceField(queryset=GrupoMercadoria.objects.all(), required = False, label = 'Grupo de Mercadoria')
	unidadeMaterial = forms.ModelChoiceField(queryset=UnidadeMaterial.objects.all(), required = False, label = 'Unidade de Medida')
	tpMaterial = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), required = False, label = 'Tipo de Material')

	fields = ('nome', 'fabricante', 'grupoMercadoria', 'unidadeMaterial', 'tpMaterial')






