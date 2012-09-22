# -* coding:utf-8 -*-

from django import forms
from models import *

class FormAdicionaCentroCusto(forms.ModelForm):
	nome_centro_custo = forms.CharField(label = 'Centro de Custo')
	grupoGerente = Group.objects.filter(name__iexact = 'gerente')
	gerente = forms.ModelChoiceField(queryset=User.objects.filter(groups__in = grupoGerente, is_active = 't').order_by('username'))
		
	class Meta:
		model = CentroCusto
		fields = ('nome_centro_custo', 'gerente')

class FormEditaCentroCusto(forms.ModelForm):
	nome_centro_custo = forms.CharField(label = 'Centro de Custo')
	grupoGerente = Group.objects.filter(name__iexact = 'gerente')
	gerente = forms.ModelChoiceField(queryset=User.objects.filter(groups__in = grupoGerente, is_active = 't').order_by('username'))
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')
	
	class Meta:
		model = CentroCusto
		fields = ('nome_centro_custo', 'gerente', 'status')

class FormExibeCentroCusto(forms.ModelForm):
	nome_centro_custo = forms.CharField(label = 'Centro de Custo')
	gerente = forms.CharField(label = 'Gerente')
	status = forms.CharField(label = 'Situação')
	
	class Meta:
		model = CentroCusto
		fields = ('nome_centro_custo', 'gerente', 'status')

class FormFiltraCentroCusto(forms.Form):
	grupoGerente = Group.objects.filter(name__iexact = 'gerente')
	nome_centro_custo = forms.CharField(label = 'Centro de Custo', required = False)
	gerente = forms.ModelChoiceField(queryset=User.objects.filter(groups__in = grupoGerente, is_active = 't').order_by('username'), label = 'Gerente', required = False)
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	class Meta:
		model = CentroCusto
		fields = ('nome_centro_custo', 'gerente', 'status')

class FormEditaCotacao(forms.ModelForm):
	vl_cotacao = forms.DecimalField(max_digits = 20, decimal_places = 2, label = 'Valor Unitário')
	
	class Meta:
		model = Cotacao
		fields = ('vl_cotacao', 'obs')

class FormExibeCotacao(forms.ModelForm):
	vl_cotacao = forms.DecimalField(max_digits = 20, decimal_places = 2, label = 'Valor Unitário')
	item_requisicao = forms.CharField(label = 'Item da Cotação')
	dt_limite = forms.CharField(label = 'Data Limite')

	class Meta:
		model = Cotacao
		fields = ('item_requisicao', 'dt_limite', 'vl_cotacao', 'obs')

class FormFiltraCotacao(forms.Form):
	vl_cotacaoP = forms.DecimalField(max_digits = 20, decimal_places = 2, required = False, label = 'Valor Unitário a partir de')
	vl_cotacaoA = forms.DecimalField(max_digits = 20, decimal_places = 2, required = False, label = 'Valor Unitário ate')
	dt_limiteP = forms.DateField(
				label = 'Data limite a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dt_limiteA = forms.DateField(
				label = 'Data limite ate',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	item_requisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Cotação')
	
	
	fields = ('dt_limiteP', 'dt_limiteA', 'dt_limiteP', 'dt_limiteA', 'item_requisicao')

class FormAdicionaFabricante(forms.ModelForm):
	nome_fabricante = forms.CharField(label = 'Fabricante')
	
	class Meta:
		model = Fabricante
		fields = ('nome_fabricante',)

class FormEditaFabricante(forms.ModelForm):
	nome_fabricante = forms.CharField(label = 'Fabricante')
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')

	class Meta:
		model = Fabricante
		fields = ('nome_fabricante', 'status')

class FormExibeFabricante(forms.ModelForm):
	nome_fabricante = forms.CharField(label = 'Fabricante')
	status = forms.CharField(label = 'Situação')

	class Meta:
		model = Fabricante
		fields = ('nome_fabricante', 'status')

class FormFiltraFabricante(forms.Form):
	nome_fabricante = forms.CharField(label = 'Fabricante', required = False)
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	fields = ('nome_fabricante', 'status')

class FormAdicionaFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	grupoFornecedor = Group.objects.filter(name__iexact = 'fornecedor')
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

class FormEditaFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	grupoFornecedor = Group.objects.filter(name__iexact = 'fornecedor')
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
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Suspenso','Suspenso'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'tel1', 'tel2', 'email', 'site', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep', 'status')

class FormExibeFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	usuario =  forms.CharField(label = 'Login no Sistema')
	tel1 = forms.CharField(min_length = 10, max_length = 10)
	tel2 = forms.CharField(min_length = 10, max_length = 10)
	nrimovel = forms.IntegerField(label = 'Nº')
	complemento = forms.CharField(max_length = 50, required = False)
	uf = forms.CharField(label = 'Estado')
	status = forms.CharField(label = 'Situação')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'tel1', 'tel2', 'email', 'site', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep', 'status')

class FormFiltraFornecedor(forms.Form):
	razao = forms.CharField(label = 'Razão Social', required = False)
	fantasia = forms.CharField(label = 'Nome Fantasia', required = False)
	cnpj = forms.CharField(min_length = 14, max_length = 14, label = 'CNPJ', required = False)
	grupoFornecedor = Group.objects.filter(name = 'fornecedor')
	usuario =  forms.ModelChoiceField(queryset = User.objects.filter(groups__in = grupoFornecedor), required = False, label = 'Login no Sistema')
	bairro = forms.CharField(label = 'Bairro', required = False)
	cidade = forms.CharField(label = 'Cidade', required = False)
	uf = forms.ChoiceField([('',''), ('AC','AC'), ('AL','AL'), ('AM','AM'),
				('AP','AP'),('BA','BA'), ('CE','CE'), ('DF','DF'),
				('ES','ES'),('GO','GO'), ('MA','MA'), ('MG','MG'),
				('MS','MS'),('MT','MT'), ('PA','PA'), ('PB','PB'),
				('PI','PI'),('PI','PI'), ('PR','PR'), ('RJ','RJ'),
				('RN','RN'),('RO','RO'), ('RR','RR'), ('RS','RS'),
				('SC','SC'),('SE','SE'),('SP','SP'), ('TO','TO')], 
				initial = ('',''),
				label = 'Estado', required = False)
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Suspenso','Suspenso'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)

	fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'bairro', 'cidade', 'uf', 'status')

class FormGruposFornecedor(forms.ModelForm):

	class Meta:
		model = Fornecedor
		fields = ('grupo_mercadoria',)

class FormAdicionaGrupoMercadoria(forms.ModelForm):
	nome_grupo_mercadoria = forms.CharField(label = 'Grupo de Mercadoria')
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nome_grupo_mercadoria',)

class FormEditaGrupoMercadoria(forms.ModelForm):
	nome_grupo_mercadoria = forms.CharField(label = 'Grupo de Mercadoria')
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nome_grupo_mercadoria','status')

class FormExibeGrupoMercadoria(forms.ModelForm):
	nome_grupo_mercadoria = forms.CharField(label = 'Grupo de Mercadoria')
	status = forms.CharField(label = 'Situação')
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nome_grupo_mercadoria','status')

class FormFiltraGrupoMercadoria(forms.Form):
	nome_grupo_mercadoria = forms.CharField(label = 'Grupo de Mercadoria', required = False)
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	fields = ('nome_grupo_mercadoria', 'status')

class FormItemRequisicao(forms.ModelForm):
	material = forms.ModelChoiceField(queryset=Material.objects.all(), label = 'Material / Serviço')
	qtd = forms.IntegerField(label = 'Quantidade')
	
	class Meta:
		model = ItemRequisicao
		fields = ('material', 'qtd')

class FormAdicionaMaterial(forms.ModelForm):
	nome_material = forms.CharField(label = 'Nome')
	fabricante = forms.ModelChoiceField(queryset = Fabricante.objects.filter(status = 'Ativo'), label = 'Fabricante')
	unidade_medida = forms.ModelChoiceField(queryset = UnidadeMedida.objects.filter(status = 'Ativo'), label = 'Unidade de Medida')
	grupo_mercadoria = forms.ModelChoiceField(queryset = GrupoMercadoria.objects.filter(status = 'Ativo'), label = 'Grupo de Mercadoria')
	tp_material = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), label = 'Tipo de Material')

	class Meta:
		model = Material
		fields = ('nome_material', 'fabricante', 'grupo_mercadoria', 'unidade_medida', 'tp_material')

class FormEditaMaterial(forms.ModelForm):
	nome_material = forms.CharField(label = 'Nome')
	fabricante = forms.ModelChoiceField(queryset = Fabricante.objects.filter(status = 'Ativo'), label = 'Fabricante')
	unidade_medida = forms.ModelChoiceField(queryset = UnidadeMedida.objects.filter(status = 'Ativo'), label = 'Unidade de Medida')
	grupo_mercadoria = forms.ModelChoiceField(queryset = GrupoMercadoria.objects.filter(status = 'Ativo'), label = 'Grupo de Mercadoria')
	tp_material = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), label = 'Tipo de Material')
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')

	class Meta:
		model = Material
		fields = ('nome_material', 'fabricante', 'grupo_mercadoria', 'unidade_medida', 'tp_material', 'status')

class FormExibeMaterial(forms.ModelForm):
	nome_material = forms.CharField(label = 'Nome')
	fabricante = forms.CharField(label = 'Fabricante')
	unidade_medida = forms.CharField(label = 'Unidade de Medida')
	grupo_mercadoria = forms.CharField(label = 'Grupo de Mercadoria')
	tp_material = forms.CharField(label = 'Tipo de Material')
	status = forms.CharField(label = 'Situação')

	class Meta:
		model = Material
		fields = ('nome_material', 'fabricante', 'grupo_mercadoria', 'unidade_medida', 'tp_material', 'status')

class FormFiltraMaterial(forms.Form):	
	nome_material = forms.CharField(label = 'Nome', required = False)
	fabricante = forms.ModelChoiceField(queryset=Fabricante.objects.all(), required = False, label = 'Fabricante')
	grupo_mercadoria = forms.ModelChoiceField(queryset=GrupoMercadoria.objects.all(), required = False, label = 'Grupo de Mercadoria')
	unidade_medida = forms.ModelChoiceField(queryset=UnidadeMedida.objects.all(), required = False, label = 'Unidade de Medida')
	tp_material = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), required = False, label = 'Tipo de Material')
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)

	fields = ('nome_material', 'fabricante', 'grupo_mercadoria', 'unidade_medida', 'tp_material', 'status')

class FormMapaComparativo(forms.ModelForm):
	
	class Meta:
		model = MapaComparativo
		fields = ('obs',)

class FormExibeMapaComparativo(forms.ModelForm):
	dt_liberacao = forms.CharField(label = 'Liberação do Mapa')
	cotacao_vencedora = forms.CharField(label = 'Cotação Vencedora')


	class Meta:
		model = MapaComparativo
		fields = ('dt_liberacao', 'cotacao_vencedora', 'obs')

class FormFiltraMapaComparativo(forms.Form):
	dt_liberacaoP = forms.DateField(
				label = 'Liberacao a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dt_liberacaoA = forms.DateField(
				label = 'Liberacao até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	fornecedorVencedor = forms.ModelChoiceField(queryset=Fornecedor.objects.all(), required = False, label = 'Forncedor Vencedor')
	status = forms.ChoiceField([('',' ------- '), ('Aberto','Aberto'), ('Aguardando Aprovação','Aguardando Aprovação'), 					('Finalizado','Finalizado')], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	
	fields = ('dt_liberacaoP', 'dt_liberacaoA', 'fornecedorVencedor', 'status')

class FormRequisicao(forms.ModelForm):
	centro_custo = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), label = 'Centro de Custo')
	dias_para_cotacao = forms.IntegerField(label = 'Nº de dias para cotação')

	class Meta:
		model = Requisicao
		fields = ('centro_custo', 'dias_para_cotacao')

class FormEditaRequisicao(forms.ModelForm):
	centro_custo = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), label = 'Centro de Custo')
	dias_para_cotacao = forms.IntegerField(label = 'Nº de dias para cotação')
	status = forms.ChoiceField([('',''), ('Aprovada','Aprovada'), ('Aguardando Aprovação','Aguardando Aprovação'), ('Reprovada','Reprovada'), ('Excluido','Excluido')], 
				initial = ('',''),
				label = 'Situação', required = False)

	class Meta:
		model = Requisicao
		fields = ('centro_custo', 'dias_para_cotacao', 'status')

class FormFiltraRequisicao(forms.Form):
	dt_requisicaoP = forms.DateField(
				label = 'Criação a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dt_requisicaoA = forms.DateField(
				label = 'Criação até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dt_deferimentoP = forms.DateField(
				label = 'Deferimento a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dt_deferimentoA = forms.DateField(
				label = 'Deferimento até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	centro_custo = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), required = False, label = 'Centro de Custo')
	item_requisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Requisição')
	status = forms.ChoiceField([('',''), ('Aprovada','Aprovada'), ('Aguardando Aprovação','Aguardando Aprovação'), ('Reprovada','Reprovada'), ('Excluido','Excluido')], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	
	fields = ('dt_requisicaoP', 'dt_requisicaoA', 'item_requisicao', 'dt_deferimentoP', 'dt_deferimentoA', 'centro_custo')

class FormAdicionaUnidadeMedida(forms.ModelForm):
	nome_unidade_medida = forms.CharField(label = 'Unidade de Medida')
	desc_unidade_medida = forms.CharField(label = 'Descrição')
	
	class Meta:
		model = UnidadeMedida
		fields = ('nome_unidade_medida', 'desc_unidade_medida')

class FormEditaUnidadeMedida(forms.ModelForm):
	nome_unidade_medida = forms.CharField(label = 'Unidade de Medida')
	desc_unidade_medida = forms.CharField(label = 'Descrição')
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação')
	
	class Meta:
		model = UnidadeMedida
		fields = ('nome_unidade_medida', 'desc_unidade_medida', 'status')

class FormExibeUnidadeMedida(forms.ModelForm):
	nome_unidade_medida = forms.CharField(label = 'Unidade de Medida')
	desc_unidade_medida = forms.CharField(label = 'Descrição')
	status = forms.CharField(label = 'Situação')
	
	class Meta:
		model = UnidadeMedida
		fields = ('nome_unidade_medida', 'desc_unidade_medida', 'status')

class FormFiltraUnidadeMedida(forms.Form):
	nome_unidade_medida = forms.CharField(label = 'Unidade de Medida', required = False)
	desc_unidade_medida = forms.CharField(label = 'Descrição', required = False)
	status = forms.ChoiceField([('',''), ('Ativo','Ativo'), ('Excluido','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	fields = ('nome_unidade_medida', 'desc_unidade_medida', 'status')





