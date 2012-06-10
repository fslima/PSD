# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta, date
from django.core.mail import send_mail

class GrupoMercadoria(models.Model):
	def __unicode__(self):
		return self.nomeGrupoMercadoria

	nomeGrupoMercadoria = models.CharField(max_length = 50, unique = True)
	status = models.CharField(max_length = 50)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_gm', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_gm', null = True)
	dtExclusao = models.DateTimeField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_gm', null = True)
	
	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if GrupoMercadoria.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'grupo_mercadoria'

class UnidadeMedida(models.Model):
	def __unicode__(self):
		return self.nomeUnidadeMedida

	nomeUnidadeMedida = models.CharField(max_length = 50, unique = True)
	descUnidadeMedida = models.CharField(max_length = 50)
	status = models.CharField(max_length = 50)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_um', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_um', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_um', null = True)

	
	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if UnidadeMedida.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'unidade_medida'

class CentroCusto(models.Model):
	def __unicode__(self):
		return self.nomeCentroCusto

	nomeCentroCusto = models.CharField(max_length = 50, unique = True)
	gerente = models.ForeignKey(User)
	status = models.CharField(max_length = 50)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_cc', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_cc', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_cc', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if CentroCusto.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'centro_custo'

class Fabricante(models.Model):
	def __unicode__(self):
		return self.nomeFabricante

	nomeFabricante = models.CharField(max_length = 50, unique = True)
	status = models.CharField(max_length = 50)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_fab', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_fab', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_fab', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if Fabricante.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	class Meta:
		db_table = 'fabricante'

class Material(models.Model):
	def __unicode__(self):
		return self.nomeMaterial
	
	nomeMaterial = models.CharField(max_length = 50, unique = True)
	fabricante = models.ForeignKey(Fabricante, related_name = 'fabricante_material')
	grupoMercadoria = models.ForeignKey(GrupoMercadoria, related_name = 'gm_material')
	unidadeMedida = models.ForeignKey(UnidadeMedida, related_name = 'un_material')
	tpMaterial = models.CharField(max_length = 50)
	status = models.CharField(max_length = 50)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_mat', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_mat', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_mat', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if Material.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
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
	grupoMercadoria = models.ManyToManyField(GrupoMercadoria, related_name = 'gm_fornecedor')
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

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_for', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_for', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_for', null = True)	

	def adicionar(self, request, idObjeto):
		self.status = u'Ativo'
		self.usuarioInclusao = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if Fornecedor.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'	

	class Meta:
		db_table = 'fornecedor'

class Requisicao(models.Model):
	def __unicode__(self):
		return str(self.id)

	dtRequisicao = models.DateField()
	centroCusto = models.ForeignKey(CentroCusto, related_name = 'cc_requisicao')
	solicitante = models.ForeignKey(User)
	status = models.CharField(max_length = 50)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	dtExclusao = models.DateField(null = True)
	dtDeferimento = models.DateField(null = True)
	diasParaCotacao = models.PositiveSmallIntegerField()

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_req', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_req', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_req', null = True)	

	def adicionar(self, request, idObjeto):
		self.dtRequisicao = datetime.now()
		self.status = u'Aguardando Aprovação'
		self.solicitante = request.user
		self.save()
		return 'validos'

	def editar(self, request, idObjeto):
		if self.status not in [u'Excluido', u'Aguardando Aprovação']:
			return 'Só é possível alterar situação para Excluido ou Aguardando Aprovação'
		if self.status == u'Excluido':
			self.dtExclusao = datetime.now()
			self.usuarioExclusao = request.user
		if Requisicao.objects.get(pk = idObjeto).status == u'Excluido' and self.status != u'Excluido' and self.status != u'Excluido':
			self.usuarioExclusao = None
			self.dtExclusao = None
		self.usuarioAlteracao = request.user
		self.save()
		return 'validos'

	def excluir(self, request, idObjeto):
		if self.status == 'Aprovada':
			return 'Não é possível excluir requisição aprovada'
		self.dtExclusao = datetime.now()
		self.usuarioExclusao = request.user
		self.status = u'Excluido'
		self.save()
		return 'validos'

	def aprovar(self):
		if self.status == u'Aguardando Aprovação':
			itens = ItemRequisicao.objects.filter(requisicao = self)
			for item in itens:
				if Cotacao().adicionar(item, self.diasParaCotacao) != 'Validos':
					return Cotacao().adicionar(item, self.diasParaCotacao)
			self.status = 'Aprovada'
			self.dtDeferimento = datetime.now()
			self.save()
			return 'Validos'
		return 'Requisição já está aprovada'

	def reprovar(self):
		if self.status == u'Aguardando Aprovação':
			self.status = 'Reprovada'
			self.dtDeferimento = datetime.now()
			self.save()
			return 'Validos'
		return 'Requisição deve estar aguardando aprovação'

	class Meta:
		db_table = 'requisicao'
		permissions = [('aprovar_requisicao', 'Pode aprovar requisicao')]

class ItemRequisicao(models.Model):
	def __unicode__(self):
		return self.material.nomeMaterial

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
		return str(self.dtLimite)

	itemRequisicao = models.ForeignKey(ItemRequisicao, related_name = 'item_proposta')
	fornecedor = models.ForeignKey(Fornecedor, related_name = 'fornecedor_proposta')
	vlCotacao = models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
	dtLimite = models.DateField()
	obs = models.TextField(max_length = 100, null = True)

	dtInclusao = models.DateTimeField(null = True, auto_now_add = True)
	usuarioInclusao = models.ForeignKey(User, related_name = 'incluiu_cot', null = True)
	dtAlteracao = models.DateTimeField(null = True, auto_now = True)
	usuarioAlteracao = models.ForeignKey(User, related_name = 'alterou_cot', null = True)
	dtExclusao = models.DateField(null = True)
	usuarioExclusao = models.ForeignKey(User, related_name = 'excluiu_cot', null = True)

	def adicionar(self, item, diasParaCotacao):
		fornecedores = Fornecedor.objects.filter(grupoMercadoria = item.material.grupoMercadoria, status = 'Ativo')
		if len(fornecedores) == 0:
			return 'Não há fornecedores para o item: '+str(item)
		for fornecedor in fornecedores:
			cotacao = Cotacao(itemRequisicao = item, fornecedor = fornecedor)
			cotacao.dtLimite = datetime.now() + timedelta(diasParaCotacao)
			cotacao.save()
			send_mail('SGF - Notificação de envio de cotação',
				  str(fornecedor)+',\n\nSua empresa recebeu uma nova cotação. \nVocês tem até o dia '+datetime.strftime(cotacao.dtLimite, "%d/%m/%Y")+' para enviar a resposta.\nSegue link de acesso à cotação:\nhttp://localhost:8000/edita/cotacao/'+str(cotacao.id)+' \nAguardamos a resposta à nossa Cotação.\n\nCordialmente, \nEmpresa XXX \n\n\n ESTA É UMA MENSAGEM ENVIADA AUTOMATICAMENTE PELO SISTEMA, FAVOR NÃO RESPONDER',
				  'SGF - Sistema de Gestão de Fornecedores',
				  [fornecedor.usuario.email],
				  fail_silently = False)
		MapaComparativo().adicionar(item, diasParaCotacao)
		return 'Validos'

	def editar(self, request, idObjeto):
		if self.dtLimite < date.today():
			return 'Data limite para esta cotação foi'+str(self.dtLimite)
		self.save()
		return 'validos'

	class Meta:
		db_table = 'cotacao'

class MapaComparativo(models.Model):
	def __unicode__(self):
		return str(self.id)

	cotacoes = models.ManyToManyField(Cotacao, related_name = 'cotacoes_do_mapa', null = True)
	cotacaoVencedora = models.ForeignKey(Cotacao, related_name = 'cotacao_vencedora', null = True)
	dtLiberacao = models.DateField()
	obs = models.TextField(max_length = 100, null = True)
	status = models.CharField(max_length = 50)

	def adicionar(self, item, diasParaCotacao):
		self.dtLiberacao = datetime.now() + timedelta(diasParaCotacao)
		self.status = 'Aberto'
		self.save()
		cotacoes = Cotacao.objects.filter(itemRequisicao = item)
		for cotacao in cotacoes:
			self.cotacoes.add(cotacao)

	def finalizar(self):
		self.cotacoes.all()[0].itemRequisicao.alterarStatus('Mapa Aguardando Aprovação')
		self.status = u'Aguardando Aprovação'
		self.save()

	def aprovar(self):
		if self.status == u'Aguardando Aprovação':
			self.cotacoes.all()[0].itemRequisicao.alterarStatus('Mapa Finalizado')
			self.status = u'Finalizado'
			self.save()
			return 'Validos'
		return 'Mapa não foi finalizado ou já está aprovado'

	class Meta:
		db_table = 'mapa_comparativo'
		permissions = [('finalizar_mapacomparativo', 'Pode finalizar mapa comparativo'), ('aprovar_mapacomparativo', 'Pode aprovar mapa comparativo')]









