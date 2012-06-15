# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta, date
from django.core.mail import send_mail

class GrupoMercadoria(models.Model):
	def __unicode__(self):
		return self.nome_grupo_mercadoria

	nome_grupo_mercadoria = models.CharField(max_length = 50, unique = True)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_gm', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_gm', null = True)
	dt_exclusao = models.DateTimeField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_gm', null = True)
	
	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if GrupoMercadoria.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'grupo_mercadoria'

class UnidadeMedida(models.Model):
	def __unicode__(self):
		return self.nome_unidade_medida

	nome_unidade_medida = models.CharField(max_length = 50, unique = True)
	desc_unidade_medida = models.CharField(max_length = 50)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_um', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_um', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_um', null = True)

	
	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if UnidadeMedida.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'unidade_medida'

class CentroCusto(models.Model):
	def __unicode__(self):
		return self.nome_centro_custo

	nome_centro_custo = models.CharField(max_length = 50, unique = True)
	gerente = models.ForeignKey(User)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_cc', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_cc', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_cc', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if CentroCusto.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'centro_custo'

class Fabricante(models.Model):
	def __unicode__(self):
		return self.nome_fabricante

	nome_fabricante = models.CharField(max_length = 50, unique = True)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_fab', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_fab', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_fab', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if Fabricante.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'fabricante'

class Material(models.Model):
	def __unicode__(self):
		return self.nome_material
	
	nome_material = models.CharField(max_length = 50, unique = True)
	fabricante = models.ForeignKey(Fabricante, related_name = 'fabricante_material')
	grupo_mercadoria = models.ForeignKey(GrupoMercadoria, related_name = 'gm_material')
	unidade_medida = models.ForeignKey(UnidadeMedida, related_name = 'un_material')
	tp_material = models.CharField(max_length = 50)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_mat', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_mat', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_mat', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if Material.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'
	
	class Meta:
		db_table = 'material'

class Fornecedor(models.Model):
	def __unicode__(self):
		return self.fantasia
	
	razao = models.CharField(max_length = 50, unique = True)
	fantasia = models.CharField(max_length = 50, unique = True)
	cnpj = models.CharField(max_length = 14, unique = True)
	grupo_mercadoria = models.ManyToManyField(GrupoMercadoria, related_name = 'gm_fornecedor')
	usuario = models.OneToOneField(User)
	tel1 = models.BigIntegerField(max_length = 10)
	tel2 = models.BigIntegerField(max_length = 10, null = True, blank = True)
	email = models.EmailField(max_length = 50)
	site = models.URLField(null = True)
	logradouro = models.CharField(max_length = 50)
	nrimovel = models.IntegerField()
	complemento = models.CharField(max_length = 50)
	bairro = models.CharField(max_length = 50)
	cidade = models.CharField(max_length = 50)
	uf = models.CharField(max_length = 2)
	cep = models.BigIntegerField(max_length = 8)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_for', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_for', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_for', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if Fornecedor.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'	

	class Meta:
		db_table = 'fornecedor'
		permissions = [('change_gruposfornecedor', 'Pode alterar grupos de mercadoria do fornecedor')]

class Requisicao(models.Model):
	def __unicode__(self):
		return str(self.id)

	dt_requisicao = models.DateField()
	centro_custo = models.ForeignKey(CentroCusto, related_name = 'cc_requisicao')
	solicitante = models.ForeignKey(User)
	status = models.CharField(max_length = 50)
	dt_deferimento = models.DateField(null = True)
	dias_para_cotacao = models.PositiveSmallIntegerField()

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuario_inclusao = models.ForeignKey(User, related_name = 'incluiu_req', null = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_req', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_req', null = True)	

	def adicionar(self, request, idObjeto):
		self.dt_requisicao = datetime.now()
		self.status = u'Aguardando Aprovação'
		self.solicitante = request.user
		self.usuario_inclusao = request.user
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status not in [u'Excluido', u'Aguardando Aprovação']:
			return 'Só é possível alterar situação para Excluido ou Aguardando Aprovação'
		if self.status == u'Excluido':
			self.dt_exclusao = datetime.now()
			self.usuario_exclusao = request.user
		if Requisicao.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido' and self.status != u'Excluido':
			self.usuario_exclusao = None
			self.dt_exclusao = None
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		if self.status == 'Aprovada':
			return 'Não é possível excluir requisição aprovada'
		self.dt_exclusao = datetime.now()
		self.usuario_exclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	def aprovar(self, request):
		if self.status == u'Aguardando Aprovação':
			itens = ItemRequisicao.objects.filter(requisicao = self)
			for item in itens:
				if Cotacao().adicionar(item, self.dias_para_cotacao) != 'Validos':
					return Cotacao().adicionar(item, self.dias_para_cotacao)
			self.status = 'Aprovada'
			self.dt_deferimento = datetime.now()
			self.usuario_alteracao = request.user
			self.save()
			return 'Validos'
		return 'Requisição já está aprovada'

	def reprovar(self, request):
		if self.status == u'Aguardando Aprovação':
			self.status = 'Reprovada'
			self.dt_deferimento = datetime.now()
			self.usuario_alteracao = request.user
			self.save()
			return 'Validos'
		return 'Requisição deve estar aguardando aprovação'

	class Meta:
		db_table = 'requisicao'
		permissions = [('aprovar_requisicao', 'Pode aprovar requisicao')]

class ItemRequisicao(models.Model):
	def __unicode__(self):
		return self.material.nome_material

	requisicao = models.ForeignKey(Requisicao, related_name = 'requisicao_do_item')
	material = models.ForeignKey(Material, related_name = 'material_do_item')
	qtd = models.PositiveSmallIntegerField()
	status = models.CharField(max_length = 50)

	def adicionar(self, request, idObjeto):
		self.requisicao = Requisicao.objects.get(pk = idObjeto)
		self.status = 'Aguardando Cotações'
		self.save()
		return 'validos'

	def alterarStatus(self, status):
		self.status = status
		self.save()

	class Meta:
		db_table = 'item_requisicao'

class Cotacao(models.Model):
	def __unicode__(self):
		return str(self.dt_limite)

	item_requisicao = models.ForeignKey(ItemRequisicao, related_name = 'item_proposta')
	fornecedor = models.ForeignKey(Fornecedor, related_name = 'fornecedor_proposta')
	vl_cotacao = models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
	dt_limite = models.DateField()
	obs = models.TextField(max_length = 100, null = True)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_cot', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_cot', null = True)

	def adicionar(self, item, dias_para_cotacao):
		fornecedores = Fornecedor.objects.filter(grupo_mercadoria = item.material.grupo_mercadoria, status = 'Ativo')
		if len(fornecedores) == 0:
			return 'Não há fornecedores para o item: '+str(item)
		for fornecedor in fornecedores:
			cotacao = Cotacao(item_requisicao = item, fornecedor = fornecedor)
			cotacao.dt_limite = datetime.now() + timedelta(dias_para_cotacao)
			if fornecedor.usuario.email:
				send_mail('SGF - Notificação de envio de cotação',
					  str(fornecedor)+',\n\nSua empresa recebeu uma nova cotação. \nVocês tem até o dia '+datetime.strftime(cotacao.dt_limite, "%d/%m/%Y")+' para enviar a resposta.\nSegue link de acesso à cotação:\nhttp://localhost:8000/edita/cotacao/'+str(cotacao.id)+' \nAguardamos a resposta à nossa Cotação.\n\nCordialmente, \nEmpresa XXX \n\n\n ESTA É UMA MENSAGEM ENVIADA AUTOMATICAMENTE PELO SISTEMA, FAVOR NÃO RESPONDER',
					  'SGF - Sistema de Gestão de Fornecedores',
					  [fornecedor.usuario.email],
					  fail_silently = True)
			cotacao.save()
		MapaComparativo().adicionar(item, dias_para_cotacao)
		return 'Validos'

	def editar(self, request, idObjeto):
		if self.dt_limite < date.today():
			return 'Data limite para esta cotação foi'+str(self.dt_limite)
		self.usuario_alteracao = request.user
		self.save()
		return 'validos'

	class Meta:
		db_table = 'cotacao'

class MapaComparativo(models.Model):
	def __unicode__(self):
		return str(self.id)

	cotacoes = models.ManyToManyField(Cotacao, related_name = 'cotacoes_do_mapa', null = True)
	cotacao_vencedora = models.ForeignKey(Cotacao, related_name = 'cotacao_vencedora', null = True)
	dt_liberacao = models.DateField()
	centro_custo = models.ForeignKey(CentroCusto, related_name = 'cc_mapa')
	obs = models.TextField(max_length = 100, null = True)
	status = models.CharField(max_length = 50)

	dt_inclusao = models.DateTimeField(null = True, auto_now_add = True)
	dt_alteracao = models.DateTimeField(null = True, auto_now = True)
	usuario_alteracao = models.ForeignKey(User, related_name = 'alterou_mapa', null = True)
	dt_exclusao = models.DateField(null = True)
	usuario_exclusao = models.ForeignKey(User, related_name = 'excluiu_mapa', null = True)

	def adicionar(self, item, dias_para_cotacao):
		self.dt_liberacao = datetime.now() + timedelta(dias_para_cotacao)
		self.status = 'Aberto'
		self.centro_custo = item.requisicao.centro_custo
		self.save()
		cotacoes = Cotacao.objects.filter(item_requisicao = item)
		for cotacao in cotacoes:
			self.cotacoes.add(cotacao)

	def finalizar(self, request):
		self.cotacoes.all()[0].item_requisicao.alterarStatus('Mapa Aguardando Aprovação')
		self.status = u'Aguardando Aprovação'
		self.usuario_alteracao = request.user
		self.save()

	def aprovar(self, request):
		if self.status == u'Aguardando Aprovação':
			self.cotacoes.all()[0].item_requisicao.alterarStatus('Mapa Finalizado')
			self.status = u'Finalizado'
			self.usuario_alteracao = request.user
			self.save()
			return 'Validos'
		return 'Mapa não foi finalizado ou já está aprovado'

	def reprovar(self, request):
		if self.status == u'Aguardando Aprovação':
			self.status = 'Reprovado'
			self.dt_deferimento = datetime.now()
			self.usuario_alteracao = request.user
			self.save()
			return 'Validos'
		return 'Mapa Comparativo deve estar aguardando aprovação'

	class Meta:
		db_table = 'mapa'
		permissions = [('finalizar_mapa', 'Pode finalizar mapa comparativo'), ('aprovar_mapa', 'Pode aprovar mapa comparativo')]









