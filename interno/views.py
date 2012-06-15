# -*- coding:utf-8 -*-

from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from django.template import RequestContext
from forms import *

def sair(request):
	logout(request)
	return HttpResponseRedirect("/")

@login_required
def inicio(request):
	data = datetime.now()
	return render_to_response('inicio.html', locals(), context_instance = RequestContext(request))

@login_required
def cadastro(request):
	return render_to_response('cadastro.html', locals(), context_instance = RequestContext(request))

@login_required
def adiciona(request, tpObjeto, idObjeto):
	if not request.user.has_perm('interno.add_'+str(tpObjeto)):
			erro = 'Você não possui acesso para cadastrar '+str(tpObjeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(tpObjeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		formpost = FormAdicionaGrupoMercadoria(request.POST, request.FILES)
		formget = FormAdicionaGrupoMercadoria()
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida do Material'
		formpost = FormAdicionaUnidadeMedida(request.POST, request.FILES)
		formget = FormAdicionaUnidadeMedida()	
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		formpost = FormAdicionaCentroCusto(request.POST, request.FILES, )
		formget = FormAdicionaCentroCusto()
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		formpost = FormAdicionaFabricante(request.POST, request.FILES, )
		formget = FormAdicionaFabricante()
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		formpost = FormAdicionaMaterial(request.POST, request.FILES, )
		formget = FormAdicionaMaterial()
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		formpost = FormAdicionaFornecedor(request.POST, request.FILES, )
		formget = FormAdicionaFornecedor()
	if str(tpObjeto) == 'requisicao':
		titulo = 'Requisicao'
		formpost = FormRequisicao(request.POST, request.FILES, )
		formget = FormRequisicao()
	if str(tpObjeto) == 'itemrequisicao':
		requisicao = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		if requisicao.status == 'Aprovada':
			erro = 'Não é possível inserir item em cotação Aprovada'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		titulo = 'Itens da Requisicao'
		formpost = FormItemRequisicao(request.POST, request.FILES, )
		formget = FormItemRequisicao()
		formRequisicao = FormRequisicao(instance = requisicao)
		itens = ItemRequisicao.objects.filter(requisicao = requisicao)
	if str(tpObjeto) == 'mapacomparativo':
		erro = 'Não é possível cadastrar mapa manualmente'
		return render_to_response('500.html', locals(), context_instance = RequestContext(request))
	if request.method == 'POST': 
		form = formpost
		if form.is_valid():
			objeto_form = form.save(commit = False)
			if objeto_form.adicionar(request, idObjeto) != 'validos':
				erro =  objeto_form.adicionar(request, idObjeto)
				return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
			if str(tpObjeto) == 'requisicao':
				return HttpResponseRedirect("/adiciona/itemrequisicao/"+str(objeto_form.id))
			if str(tpObjeto) == 'itemrequisicao':
				return HttpResponseRedirect("/adiciona/itemrequisicao/"+str(idObjeto))
			if str(tpObjeto) == 'fornecedor':
				return HttpResponseRedirect("/edita/gruposfornecedor/"+str(objeto_form.id))
			return HttpResponseRedirect("/lista/"+str(tpObjeto))
		else:
			return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
	else: 
		form = formget
		return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))

@login_required
def lista(request, tpObjeto):
	if str(tpObjeto) == 'grupomercadoria':
		titulo = 'Cadastro de Grupos de Mercadoria'
		listaVazia = 'Nenhum Grupo de Mercadoria Cadastrado'
		lista = GrupoMercadoria.objects.filter(status = 'Ativo').order_by('nome_grupo_mercadoria')
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Cadastro de Unidades de Medida do Material'
		listaVazia = 'Nenhuma Unidade de Medida Cadastrada'
		lista = UnidadeMedida.objects.filter(status = 'Ativo').order_by('nome_unidade_medida')
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Cadastro de Centros de Custo'
		listaVazia = 'Nenhum Centro de Custo Cadastrado'
		lista = CentroCusto.objects.filter(status = 'Ativo').order_by('nome_centro_custo')
	if str(tpObjeto) == 'fabricante':
		titulo = 'Cadastro de Fabricante'
		listaVazia = 'Nenhum Fabricante Cadastrado'
		lista = Fabricante.objects.filter(status = 'Ativo').order_by('nome_fabricante')
	if str(tpObjeto) == 'material':
		titulo = 'Cadastro de Materiais'
		listaVazia = 'Nenhum Material Cadastrado'
		lista = Material.objects.filter(status = 'Ativo').order_by('nome_material')
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Cadastro de Fornecedores'
		listaVazia = 'Nenhum Fornecedor Cadastrado'
		lista = Fornecedor.objects.filter(status = 'Ativo').order_by('fantasia')
	if str(tpObjeto) == 'requisicao':
		titulo = 'Requisições Em Aberto'
		listaVazia = 'Nenhuma Requisição sua está em Aberto'
		lista = Requisicao.objects.filter(solicitante = request.user).exclude(status = u'Excluido').order_by('id').reverse()
		lista1 = []
		remover = []
		manter = []
		for requisicao in lista:
			lista1.append(requisicao)
			itens = ItemRequisicao.objects.filter(requisicao = requisicao)
			for item in itens:
				if item.status == u'Mapa Finalizado':
					if requisicao not in remover:
						remover.append(requisicao)
				else:
					if requisicao not in manter:
						manter.append(requisicao)
		for requisicao in remover:
			if requisicao not in manter:
				lista1.remove(requisicao)
		lista = lista1
	if str(tpObjeto) == 'mapacomparativo':
		titulo = 'Lista de Mapas Comparativos'
		listaVazia = 'Nenhum Mapa Cadastrado'
		lista = MapaComparativo.objects.filter(dt_liberacao__lt = datetime.now()).order_by('id').reverse()
		lista1 = []
		remover = []
		manter = []
		for mapa in lista:
			lista1.append(mapa)
			if mapa.cotacoes.all()[0].item_requisicao.status == u'Mapa Finalizado' or mapa.cotacoes.all()[0].item_requisicao.requisicao.solicitante != request.user:
					if mapa not in remover:
						remover.append(mapa)
					else:
						if mapa not in manter:
							manter.append(mapa)
		for mapa in remover:
			if mapa not in manter:
				lista1.remove(mapa)
		lista = lista1

	if str(tpObjeto) == 'cotacao':
		titulo = 'Itens para Cotação'
		listaVazia = 'Nenhum item para cotação'
		fornecedor = Fornecedor.objects.filter(usuario = request.user)
		if len(fornecedor) == 0:
			erro = 'Área restrita à fornecedores'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
		else:
			fornecedor = get_object_or_404(Fornecedor, usuario = request.user)
		lista = Cotacao.objects.filter(fornecedor = fornecedor).exclude(dt_limite__lte = datetime.now() - timedelta(1)).order_by('id').reverse()
	if str(tpObjeto) == 'aprovacoes':
		if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
			erro = 'Você não é aprovador de documentos'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
		titulo = 'Aprovações Pendentes'
		centro_custo = CentroCusto.objects.filter(gerente = request.user)
		listaMapasVazia = 'Nenhum mapa pendente de aprovação'
		listaRequisicoesVazia = 'Nenhuma requisição pendente de aprovação'
		listaRequisicoes = Requisicao.objects.filter(centro_custo__in = centro_custo, status = u'Aguardando Aprovação').order_by('id').reverse()
		listaMapas = MapaComparativo.objects.filter(centro_custo__in = centro_custo, status = u'Aguardando Aprovação').order_by('id').reverse()
		return render_to_response('lista_aprovacoes.html', locals(), context_instance = RequestContext(request))
	return render_to_response('lista.html', locals(), context_instance = RequestContext(request))

def exibe(request, tpObjeto, idObjeto):
	if str(tpObjeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		objeto = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		form = FormExibeGrupoMercadoria(instance = objeto)
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida'
		objeto = get_object_or_404(UnidadeMedida, pk = idObjeto)
		form = FormExibeUnidadeMedida(instance = objeto)
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		objeto = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormExibeCentroCusto(instance = objeto)
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		objeto = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormExibeFabricante(instance = objeto)
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		objeto = get_object_or_404(Material, pk = idObjeto)
		form = FormExibeMaterial(instance = objeto)
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		objeto = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormExibeFornecedor(instance = objeto)
	if str(tpObjeto) == 'requisicao':
		titulo = 'Requisicao'
		titulo_membros = 'Itens da Requisicao'
		objeto = get_object_or_404(Requisicao, pk = idObjeto)
		itens = ItemRequisicao.objects.filter(requisicao = objeto)
		form = FormRequisicao(instance = objeto)
	if str(tpObjeto) == 'mapacomparativo':
		titulo = 'Mapa Comparativo'
		titulo_cotacoes = 'Cotacoes'
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		if objeto.dt_liberacao < date.today():
			cotacoes = objeto.cotacoes.all()
		form = FormExibeMapaComparativo(instance = objeto)
	if str(tpObjeto) == 'cotacao':
		titulo = 'Cotação'
		objeto = get_object_or_404(Cotacao, pk = idObjeto)
		form = FormExibeCotacao(instance = objeto)
	if str(tpObjeto) == 'obs':
		titulo = 'Cotação'
		objeto = get_object_or_404(Cotacao, pk = idObjeto)
		form = FormExibeCotacao(instance = objeto)
		return render_to_response('obs.html', locals(), context_instance = RequestContext(request))
	return render_to_response('exibe.html', locals(), context_instance = RequestContext(request))

@login_required
def edita(request, tpObjeto, idObjeto):
	if not request.user.has_perm('interno.change_'+str(tpObjeto)):
			erro = 'Você não possui acesso para modificar '+str(tpObjeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(tpObjeto) == 'grupomercadoria':
		grupo_mercadoria_para_editar = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		formpost = FormEditaGrupoMercadoria(request.POST, request.FILES, instance = grupo_mercadoria_para_editar)
		formget = FormEditaGrupoMercadoria(instance = grupo_mercadoria_para_editar)
		titulo = 'Grupo de Mercadoria'		
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida'
		unidade_medida_para_editar = get_object_or_404(UnidadeMedida, pk = idObjeto)
		formpost = FormEditaUnidadeMedida(request.POST, request.FILES, instance = unidade_medida_para_editar)
		formget = FormEditaUnidadeMedida(instance = unidade_medida_para_editar)	
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		centro_custo_para_editar = get_object_or_404(CentroCusto, pk = idObjeto)
		formpost = FormEditaCentroCusto(request.POST, request.FILES, instance = centro_custo_para_editar)
		formget = FormEditaCentroCusto(instance = centro_custo_para_editar)	
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		fabricante_para_editar = get_object_or_404(Fabricante, pk = idObjeto)
		formpost = FormEditaFabricante(request.POST, request.FILES, instance = fabricante_para_editar)
		formget = FormEditaFabricante(instance = fabricante_para_editar)
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		material_para_editar = get_object_or_404(Material, pk = idObjeto)
		formpost = FormEditaMaterial(request.POST, request.FILES, instance = material_para_editar)
		formget = FormEditaMaterial(instance = material_para_editar)
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = idObjeto)
		formpost = FormEditaFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormEditaFornecedor(instance = fornecedor_para_editar)
	if str(tpObjeto) == 'gruposfornecedor':
		titulo = 'Grupos de Mercadoria'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = idObjeto)
		formpost = FormGruposFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormGruposFornecedor(instance = fornecedor_para_editar)
	if str(tpObjeto) == 'requisicao':
		titulo = 'Requisicao'
		requisicao_para_editar = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		if requisicao_para_editar.status == u'Aprovada':
			erro = 'Não é possível alterar requisição já aprovada'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
		formpost = FormEditaRequisicao(request.POST, request.FILES, instance = requisicao_para_editar)
		formget = FormEditaRequisicao(instance = requisicao_para_editar)
	if str(tpObjeto) == 'mapacomparativo':
		return HttpResponseRedirect("/finaliza/mapacomparativo/"+str(idObjeto))
	if str(tpObjeto) == 'cotacao':
		titulo = 'Cotação'
		cotacao_para_editar = get_object_or_404(Cotacao, pk = idObjeto)
		if cotacao_para_editar.fornecedor.usuario != request.user:
			erro = 'Cotação de outro fornecedor'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		if cotacao_para_editar.dt_limite < date.today():
			erro = 'A data limite para esta cotação foi: '
			data = cotacao_para_editar.dt_limite
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		formpost = FormEditaCotacao(request.POST, request.FILES, instance = cotacao_para_editar)
		formget = FormEditaCotacao(instance = cotacao_para_editar)
	if request.method == 'POST':
		form = formpost
		if form.is_valid():
			if str(tpObjeto) == 'gruposfornecedor':
				objeto_form = form.save()
			else:
				objeto_form = form.save(commit = False)
				if objeto_form.editar(request, idObjeto) != 'validos':
					erro =  objeto_form.editar(request, idObjeto)
					return render_to_response("edita.html", locals(), context_instance = RequestContext(request))
			if str(tpObjeto) == 'gruposfornecedor':
				return HttpResponseRedirect("/lista/fornecedor")
			return HttpResponseRedirect("/lista/"+str(tpObjeto))
		else:
			return render_to_response('edita.html', locals(), context_instance = RequestContext(request))	
	else:
		form = formget
	return render_to_response('edita.html', locals(), context_instance = RequestContext(request))

@login_required
def deleta(request, tpObjeto, idObjeto):
	if not request.user.has_perm('interno.delete_'+str(tpObjeto)):
			erro = 'Você não possui acesso para excluir '+str(tpObjeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(tpObjeto) == 'grupomercadoria':
		objeto_para_deletar = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		form = FormExibeGrupoMercadoria(instance = objeto_para_deletar)
	if str(tpObjeto) == 'centrocusto':
		objeto_para_deletar = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormExibeCentroCusto(instance = objeto_para_deletar)
	if str(tpObjeto) == 'unidademedida':
		objeto_para_deletar = get_object_or_404(UnidadeMedida, pk = idObjeto)
		form = FormExibeUnidadeMedida(instance = objeto_para_deletar)
	if str(tpObjeto) == 'fabricante':
		objeto_para_deletar = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormExibeFabricante(instance = objeto_para_deletar)
	if str(tpObjeto) == 'material':
		objeto_para_deletar = get_object_or_404(Material, pk = idObjeto)
		form = FormExibeMaterial(instance = objeto_para_deletar)
	if str(tpObjeto) == 'fornecedor':
		objeto_para_deletar = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormExibeFornecedor(instance = objeto_para_deletar)
	if str(tpObjeto) == 'requisicao':
		objeto_para_deletar = get_object_or_404(Requisicao, pk = idObjeto)
		if objeto_para_deletar.status == u'Aprovada':
			erro = 'Não é possível alterar requisição já aprovada'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
		form = FormRequisicao(instance = objeto_para_deletar)
	if str(tpObjeto) == 'mapacomparativo':
		objeto_para_deletar = get_object_or_404(MapaComparativo, pk = idObjeto)
		form = FormMapaComparativo(instance = objeto_para_deletar)
	if request.method == 'POST':
		if objeto_para_deletar.excluir(request, idObjeto) != 'validos':
			erro =  objeto_para_deletar.excluir(request, idObjeto)
			return render_to_response("deleta.html", locals(), context_instance = RequestContext(request))
		return HttpResponseRedirect("/lista/"+str(tpObjeto))
	else:
		return render_to_response('deleta.html', locals(), context_instance = RequestContext(request))

	
@login_required
def aprova(request, tpObjeto, idObjeto):
	if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
			erro = 'Você não é aprovador de documentos'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(tpObjeto) == 'requisicao':
		titulo = 'Aprovar Requisição: '
		objeto = get_object_or_404(Requisicao, pk = idObjeto)
		itens = ItemRequisicao.objects.filter(requisicao = idObjeto)
		form = FormRequisicao(instance = objeto)
	if str(tpObjeto) == 'mapacomparativo':
		titulo = 'Aprovar Mapa: '
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		cotacoes = objeto.cotacoes.all().order_by('vl_cotacao')
		form = FormExibeMapaComparativo(instance = objeto)
	if request.method == 'POST':
		if objeto.aprovar(request) != 'Validos':
			erro =  objeto.aprovar(request)
			return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))
		return HttpResponseRedirect("/lista/aprovacoes")
	else:
		return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))

@login_required
def reprova(request, tpObjeto, idObjeto):
	if str(tpObjeto) == 'requisicao':
		titulo = 'Reprovar Requisição: '
		objeto = get_object_or_404(Requisicao, pk = idObjeto)
		itens = ItemRequisicao.objects.filter(requisicao = idObjeto)
		form = FormRequisicao(instance = objeto)
	if str(tpObjeto) == 'mapacomparativo':
		titulo = 'Reprovar Mapa: '
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		cotacoes = objeto.cotacoes.all().order_by('vl_cotacao')
		form = FormExibeMapaComparativo(instance = objeto)

	if objeto.reprovar(request) != 'Validos':
		erro =  objeto.reprovar(request)
		return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))
	return HttpResponseRedirect("/lista/aprovacoes")
	
@login_required
def filtra(request, tpObjeto):
	if str(tpObjeto) == 'material':
		titulo = 'Pesquisar Material'
		radicalObjeto = 'Materia'
		formpost = FormFiltraMaterial(request.POST, request.FILES)
		formget = FormFiltraMaterial()
		nome_material = {'nome_material': 'Nome do Material'}
		fabricante = {'fabricante': 'Fabricante'}
		grupo_mercadoria = {'grupo_mercadoria': 'Grupo de Mercadoria'}
		unidade_medida = {'unidade_medida': 'Unidade de Medida'}
		tp_material = {'tp_material': 'Tipo de Material'}
		status = {'status': 'Situação'}
		campos = [nome_material, fabricante, grupo_mercadoria, unidade_medida, tp_material, status]
		colunas = ['Nome', 'Fabricante', 'Grupo de Mercadoria', 'Unidade de Medida', 'Tipo de Material', 'status']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				nome_material = valorCampo[0]
				fabricante = valorCampo[1]
				grupo_mercadoria = valorCampo[2]
				unidade_medida = valorCampo[3]
				tp_material = valorCampo[4]
				status = valorCampo[5]
				query = Material.objects.filter(nome_material__icontains = nome_material).filter(tp_material__icontains = tp_material)
				if fabricante != None:
					query = query.filter(fabricante = fabricante)
				if unidade_medida != None:
					query = query.filter(unidade_medida = unidade_medida)
				if grupo_mercadoria != None:
					query = query.filter(grupo_mercadoria = grupo_mercadoria)
				if status != '':
					query = query.filter(status = status)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraMaterial()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'fornecedor':
		titulo = 'Pesquisar Fornecedor'
		radicalObjeto = 'Fornecedo'
		formpost = FormFiltraFornecedor(request.POST, request.FILES)
		formget = FormFiltraFornecedor()
		razao = {'razao': 'Razão Social'}
		fantasia = {'fantasia': 'Nome Fantasia'}
		cnpj = {'cnpj': 'CNPJ'}
		usuario = {'usuario': 'Usuário'}
		bairro = {'bairro': 'Bairro'}
		cidade = {'cidade': 'Cidade'}
		uf = {'uf': 'UF'}
		status = {'status': 'Status'}
		campos = [razao, fantasia, cnpj, usuario, bairro, cidade, uf, status]
		colunas = ['Razão Social', 'Nome Fantasia', 'CNPJ', 'Login', 'Bairro', 'Cidade', 'UF']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				razao = valorCampo[0]
				fantasia = valorCampo[1]
				cnpj = valorCampo[2]
				usuario = valorCampo[3]
				bairro = valorCampo[4]
				cidade = valorCampo[5]
				uf = valorCampo[6]
				status = valorCampo[7]
				query = Fornecedor.objects.filter(razao__icontains = razao).filter(fantasia__icontains = fantasia).filter(cnpj__icontains = cnpj).filter(bairro__icontains = bairro).filter(cidade__icontains = cidade).filter(uf__icontains = uf).filter(status__icontains = status)
				if usuario != None:
					query = query.filter(usuario = usuario)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraFornecedor()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'mapacomparativo':
		titulo = 'Pesquisar Mapa Comparativo'
		radicalObjeto = 'Mapa'
		formpost = FormFiltraMapaComparativo(request.POST, request.FILES)
		formget = FormFiltraMapaComparativo()
		dt_liberacaoP = {'dt_liberacaoP': 'Data de Liberação'}
		dt_liberacaoA = {'dt_liberacaoA': 'Data de Liberação'}
		fornecedor = {'fornecedorVencedor': 'Fornecedor'}
		status = {'status': 'Status'}
		campos = [dt_liberacaoP, dt_liberacaoA, fornecedor, status]
		colunas = ['Nº do Mapa', 'Data de Liberação', 'Fornecedor Vencedor', 'Item Cotado', 'Valor Cotado', 'Status do Mapa']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dt_liberacaoP = valorCampo[0]
				dt_liberacaoA = valorCampo[1]
				fornecedor = valorCampo[2]
				status = valorCampo[3]
				query = MapaComparativo.objects.all().order_by('id').reverse()
				requisicoes = Requisicao.objects.filter(solicitante = request.user)
				if requisicoes != None:
					itens = ItemRequisicao.objects.filter(requisicao__in = requisicoes)
					if itens != None:
						cotacoes = Cotacao.objects.filter(item_requisicao__in = itens)
						if cotacoes != None:
							query = query.filter(cotacoes__in = cotacoes).distinct('id')
				if dt_liberacaoP != None:
					query = query.filter(dt_liberacao__gte = dt_liberacaoP)
				if dt_liberacaoA != None:
					query = query.filter(dt_liberacao__lte = dt_liberacaoA)
				if status != '':
					query = query.filter(status = status)
				if fornecedor != None:
					cotacoes = Cotacao.objects.filter(fornecedor = fornecedor)
					query = query.filter(cotacao_vencedora__in = cotacoes)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraMapaComparativo()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'cotacao':
		titulo = 'Pesquisar Cotação'
		radicalObjeto = 'Cotaç'
		formpost = FormFiltraCotacao(request.POST, request.FILES)
		formget = FormFiltraCotacao()
		dt_limiteP = {'dt_limiteP': 'Data Limite'}
		dt_limiteA = {'dt_limiteA': 'Data Limite'}
		vl_cotacaoP = {'vl_cotacaoP': 'Valor Cotado'}
		vl_cotacaoA = {'vl_cotacaoA': 'Valor Cotado'}
		item_requisicao = {'item_requisicao': 'Item Cotado'}
		campos = [dt_limiteP, dt_limiteA, vl_cotacaoP, vl_cotacaoA, item_requisicao]
		colunas = ['Data Limite', 'Valor Cotado', 'Item da Cotação']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dt_limiteP = valorCampo[0]
				dt_limiteA = valorCampo[1]
				vl_cotacaoP = valorCampo[2]
				vl_cotacaoA = valorCampo[3]
				item_requisicao = valorCampo[4]
				fornecedor = Fornecedor.objects.filter(usuario = request.user)
				query = Cotacao.objects.filter(fornecedor = fornecedor).order_by('dt_limite').reverse()
				if dt_limiteP != None:
					query = query.filter(dt_limite__gte = dt_limiteP)
				if dt_limiteA != None:
					query = query.filter(dt_limite__lte = dt_limiteA)
				if vl_cotacaoP != None:
					query = query.filter(vl_cotacao__gte = vl_cotacaoP)
				if vl_cotacaoA != None:
					query = query.filter(vl_cotacao__lte = vl_cotacaoA)
				if item_requisicao != None:
					itens = ItemRequisicao.objects.filter(material = item_requisicao)
					query = query.filter(item_requisicao__in = itens)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraCotacao()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'requisicao':
		titulo = 'Pesquisar Requisição'
		radicalObjeto = 'Requisiç'
		formpost = FormFiltraRequisicao(request.POST, request.FILES)
		formget = FormFiltraRequisicao()
		dt_requisicaoP = {'dt_requisicaoP': 'Data da Requisição'}
		dt_requisicaoA = {'dt_requisicaoA': 'Data de Requisição'}
		dt_deferimentoP = {'dt_deferimentoP': 'Data do Deferimento'}
		dt_deferimentoA = {'dt_deferimentoA': 'Data do Deferimento'}
		centro_custo = {'centro_custo': 'Centro de Custo'}
		item_requisicao = {'item_requisicao': 'Item'}
		status = {'status': 'Situação'}
		campos = [dt_requisicaoP, dt_requisicaoA, item_requisicao, dt_deferimentoP, dt_deferimentoA, centro_custo, status]
		colunas = ['Nº Requisição', 'Data da Requisição', 'Solicitante', 'Data do Deferimento', 'Status']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dt_requisicaoP = valorCampo[0]
				dt_requisicaoA = valorCampo[1]
				item_requisicao = valorCampo[2]
				dt_deferimentoP = valorCampo[3]
				dt_deferimentoA = valorCampo[4]
				centro_custo = valorCampo[5]
				status = valorCampo[6]
				query = Requisicao.objects.filter(status__icontains = status, solicitante = request.user).order_by('id').reverse()
				if dt_requisicaoP != None:
					query = query.filter(dt_requisicao__gte = dt_requisicaoP)
				if dt_requisicaoA != None:
					query = query.filter(dt_requisicao__lte = dt_requisicaoA)
				if dt_deferimentoP != None:
					query = query.filter(dt_deferimento__gte = dt_deferimentoP)
				if dt_deferimentoA != None:
					query = query.filter(dt_deferimento__lte = dt_deferimentoA)
				if centro_custo != None:
					query = query.filter(centro_custo = centro_custo)
				if item_requisicao != None:
					itens = ItemRequisicao.objects.filter(requisicao__in = query, material = item_requisicao)
					listaIdRequisicao = []
					for idRequisicao in itens:
						listaIdRequisicao.append(idRequisicao.requisicao.id)
					query = query.filter(pk__in = listaIdRequisicao)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraRequisicao()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'fabricante':
		titulo = 'Pesquisar Fabricante'
		radicalObjeto = 'Fabricante'
		formpost = FormFiltraFabricante(request.POST, request.FILES)
		formget = FormFiltraFabricante()
		nome_fabricante = {'nome_fabricante': 'Nome do Fabricante'}
		status = {'status': 'Situação'}
		campos = [nome_fabricante, status]
		colunas = ['Fabricante', 'status']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				nome_fabricante = valorCampo[0]
				status = valorCampo[1]
				query = Fabricante.objects.filter(nome_fabricante__icontains = nome_fabricante).order_by('nome_fabricante')
				if status != '':
					query = query.filter(status = status)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraFabricante()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'unidademedida':
		titulo = 'Pesquisar Unidade de Medida'
		radicalObjeto = 'Unidad'
		formpost = FormFiltraUnidadeMedida(request.POST, request.FILES)
		formget = FormFiltraUnidadeMedida()
		nome_unidade_medida = {'nome_unidade_medida': 'Unidade de Medida'}
		desc_unidade_medida = {'desc_unidade_medida': 'Descrição'}
		status = {'status': 'Situação'}
		campos = [nome_unidade_medida, desc_unidade_medida, status]
		colunas = ['Unidade de Medida', 'Descrição', 'Situação']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				nome_unidade_medida = valorCampo[0]
				desc_unidade_medida = valorCampo[1]
				status = valorCampo[2]
				query = UnidadeMedida.objects.filter(nome_unidade_medida__icontains = nome_unidade_medida).filter(nome_unidade_medida__icontains = nome_unidade_medida).order_by('desc_unidade_medida')
				if status != '':
					query = query.filter(status = status)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraUnidadeMedida()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'grupomercadoria':
		titulo = 'Pesquisar Grupo de Mercadoria'
		radicalObjeto = 'Grup'
		formpost = FormFiltraGrupoMercadoria(request.POST, request.FILES)
		formget = FormFiltraGrupoMercadoria()
		nome_grupo_mercadoria = {'nome_grupo_mercadoria': 'Grupo de Mercadoria'}
		status = {'status': 'Situação'}
		campos = [nome_grupo_mercadoria, status]
		colunas = ['Grupo de Mercadoria', 'Situação']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				nome_grupo_mercadoria = valorCampo[0]
				status = valorCampo[1]
				query = GrupoMercadoria.objects.filter(nome_grupo_mercadoria__icontains = nome_grupo_mercadoria).order_by('nome_grupo_mercadoria')
				if status != '':
					query = query.filter(status = status)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraGrupoMercadoria()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'centrocusto':
		titulo = 'Pesquisar Centro de Custo'
		radicalObjeto = 'Centr'
		formpost = FormFiltraCentroCusto(request.POST, request.FILES)
		formget = FormFiltraCentroCusto()
		nome_centro_custo = {'nome_centro_custo': 'Centro de Custo'}
		gerente = {'gerente': 'Gerente'}
		status = {'status': 'Situação'}
		campos = [nome_centro_custo, gerente, status]
		colunas = ['Centro de Custo', 'Gerente', 'status']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				nome_centro_custo = valorCampo[0]
				gerente = valorCampo[1]
				status = valorCampo[2]
				query = CentroCusto.objects.filter(nome_centro_custo__icontains = nome_centro_custo).order_by('nome_centro_custo')
				if status != '':
					query = query.filter(status = status)
				if gerente != None:
					query = query.filter(gerente = gerente)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraCentroCusto()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))


@login_required
def finaliza(request, tpObjeto, idObjeto):
	if str(tpObjeto) == 'mapacomparativo':
		if not request.user.has_perm('interno.finalizar_mapa'):
			erro = 'Você não possui acesso para finalizar mapa'
			return render_to_response("500.html", locals())
		titulo = 'Mapa Comparativo'
		objetototal = 'Cotações'
		formpost = FormMapaComparativo(request.POST, request.FILES)
		formget = FormMapaComparativo()
		erro = 'Mapa não existe'
		mapa = get_object_or_404(MapaComparativo, pk = idObjeto)
		if mapa.cotacoes.all()[0].item_requisicao.requisicao.solicitante != request.user:
			erro = 'Você só possui acesso aos mapas das suas requisições'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		if mapa.dt_liberacao >= date.today():
			erro = 'Mapa só estará liberado dia: '
			data = mapa.dt_liberacao + timedelta(1)
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		query = mapa.cotacoes.all().order_by('vl_cotacao')
		if request.method == 'POST':
			form = formpost
			if form.is_valid():	
				mapa.obs = form.cleaned_data['obs']
				if int(request.POST['cotacao']) != 0:
					id_cotacao = int(request.POST['cotacao'])
					mapa.cotacao_vencedora = Cotacao.objects.get(pk = id_cotacao)
				else:
					mapa.cotacao_vencedora = None
				mapa.finalizar(request)	
				return HttpResponseRedirect("/lista/mapacomparativo")
			else:
				return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormMapaComparativo(instance = mapa)
		return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))







