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
def adiciona(request, objeto, idObjeto):
	if not request.user.has_perm('interno.add_'+str(objeto)):
			erro = 'Você não possui acesso para cadastrar '+str(objeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(objeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		formpost = FormGrupoMercadoria(request.POST, request.FILES)
		formget = FormGrupoMercadoria()
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida do Material'
		formpost = FormUnidadeMaterial(request.POST, request.FILES)
		formget = FormUnidadeMaterial()	
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		formpost = FormCentroCusto(request.POST, request.FILES, )
		formget = FormCentroCusto()
	if str(objeto) == 'fabricante':
		titulo = 'Fabricante'
		formpost = FormFabricante(request.POST, request.FILES, )
		formget = FormFabricante()
	if str(objeto) == 'material':
		titulo = 'Material'
		formpost = FormMaterial(request.POST, request.FILES, )
		formget = FormMaterial()
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		formpost = FormFornecedor(request.POST, request.FILES, )
		formget = FormFornecedor()
	if str(objeto) == 'requisicao':
		titulo = 'Requisicao'
		formpost = FormRequisicao(request.POST, request.FILES, )
		formget = FormRequisicao()
	if str(objeto) == 'itemrequisicao':
		requisicao = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		if requisicao.status == 'Aprovada':
			erro = 'Não é possível inserir item em cotação Aprovada'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		titulo = 'Itens da Requisicao'
		formpost = FormItemRequisicao(request.POST, request.FILES, )
		formget = FormItemRequisicao()
	if request.method == 'POST': 
		form = formpost
		if form.is_valid():
			objeto_form = form.save(commit = False)
			if objeto_form.adicionar(request, idObjeto) != 'validos':
				erro =  objeto_form.adicionar(request, idObjeto)
				return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
			if str(objeto) == 'requisicao':
				return HttpResponseRedirect("/adiciona/itemrequisicao/"+str(objeto_form.id))
			if str(objeto) == 'itemrequisicao':
				return HttpResponseRedirect("/lista/requisicao")
			if str(objeto) == 'fornecedor':
				return HttpResponseRedirect("/edita/gruposfornecedor/"+str(objeto_form.id))
			return HttpResponseRedirect("/lista/"+str(objeto))
		else:
			return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
	else: 
		form = formget
		return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))

@login_required
def lista(request, objeto):
	if str(objeto) == 'grupomercadoria':
		titulo = 'Cadastro de Grupos de Mercadoria'
		lista_vazia = 'Nenhum Grupo de Mercadoria Cadastrado'
		lista = GrupoMercadoria.objects.all().order_by('nomeGrupoMercadoria')
	if str(objeto) == 'unidadematerial':
		titulo = 'Cadastro de Unidades de Medida do Material'
		lista_vazia = 'Nenhuma Unidade de Medida Cadastrada'
		lista = UnidadeMaterial.objects.all().order_by('nomeUnidadeMaterial')
	if str(objeto) == 'centrocusto':
		titulo = 'Cadastro de Centros de Custo'
		lista_vazia = 'Nenhum Centro de Custo Cadastrado'
		lista = CentroCusto.objects.all().order_by('nomeCentroCusto')
	if str(objeto) == 'fabricante':
		titulo = 'Cadastro de Fabricante'
		lista_vazia = 'Nenhum Fabricante Cadastrado'
		lista = Fabricante.objects.all().order_by('nomeFabricante')
	if str(objeto) == 'material':
		titulo = 'Cadastro de Materiais'
		lista_vazia = 'Nenhum Material Cadastrado'
		lista = Material.objects.all().order_by('nomeMaterial')
	if str(objeto) == 'fornecedor':
		titulo = 'Cadastro de Fornecedores'
		lista_vazia = 'Nenhum Fornecedor Cadastrado'
		lista = Fornecedor.objects.all().order_by('fantasia')
	if str(objeto) == 'requisicao':
		titulo = 'Requisições Em Aberto'
		lista_vazia = 'Nenhuma Requisição sua está em Aberto'
		lista = Requisicao.objects.filter(solicitante = request.user).order_by('id').reverse()
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
	if str(objeto) == 'mapa':
		titulo = 'Lista de Mapas Comparativos'
		lista_vazia = 'Nenhum Mapa Cadastrado'
		lista = MapaComparativo.objects.filter(dtLiberacao__lt = datetime.now()).order_by('id').reverse()
		lista1 = []
		remover = []
		manter = []
		for mapa in lista:
			lista1.append(mapa)
			if mapa.cotacao.all()[0].itemRequisicao.status == u'Mapa Finalizado' or mapa.cotacao.all()[0].itemRequisicao.requisicao.solicitante != request.user:
					if mapa not in remover:
						remover.append(mapa)
					else:
						if mapa not in manter:
							manter.append(mapa)
		for mapa in remover:
			if mapa not in manter:
				lista1.remove(mapa)
		lista = lista1
	if str(objeto) == 'cotacao':
		titulo = 'Itens para Cotação'
		lista_vazia = 'Nenhum item para cotação'
		fornecedor = get_object_or_404(Fornecedor, usuario = request.user)
		lista = Cotacao.objects.filter(fornecedor = fornecedor).exclude(dtLimite__lte = datetime.now() - timedelta(1)).order_by('id').reverse()
	return render_to_response('lista.html', locals(), context_instance = RequestContext(request))

def exibe(request, objeto, idObjeto):
	if str(objeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		objeto = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		form = FormGrupoMercadoria(instance = objeto)
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida'
		objeto = get_object_or_404(UnidadeMaterial, pk = idObjeto)
		form = FormUnidadeMaterial(instance = objeto)
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		objeto = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormCentroCusto(instance = objeto)
	if str(objeto) == 'fabricante':
		titulo = 'Fabricante'
		objeto = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormFabricante(instance = objeto)
	if str(objeto) == 'material':
		titulo = 'Material'
		objeto = get_object_or_404(Material, pk = idObjeto)
		v = vars(objeto)
		form = FormMaterial(instance = objeto)
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		objeto = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormFornecedor(instance = objeto)
	if str(objeto) == 'requisicao':
		titulo = 'Requisicao'
		titulo_membros = 'Itens da Requisicao'
		objeto = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		itens = ItemRequisicao.objects.filter(requisicao = objeto)
		form = FormRequisicao(instance = objeto)
	if str(objeto) == 'mapa':
		titulo = 'Mapa Comparativo'
		titulo_cotacoes = 'Cotacoes'
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		cotacoes = Cotacao.objects.filter(cotacoes_do_mapa = objeto)
		form = FormExibeMapaComparativo(instance = objeto)
	if str(objeto) == 'cotacao':
		titulo = 'Cotação'
		objeto = get_object_or_404(Cotacao, pk = idObjeto)
		form = FormExibeCotacao(instance = objeto)
	return render_to_response('exibe.html', locals(), context_instance = RequestContext(request))

@login_required
def edita(request, objeto, idObjeto):
	if not request.user.has_perm('interno.change_'+str(objeto)):
			erro = 'Você não possui acesso para modificar '+str(objeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(objeto) == 'grupomercadoria':
		grupoMercadoria_para_editar = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		formpost = FormGrupoMercadoria(request.POST, request.FILES, instance = grupoMercadoria_para_editar)
		formget = FormGrupoMercadoria(instance = grupoMercadoria_para_editar)
		titulo = 'Grupo de Mercadoria'		
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida'
		unidadeMaterial_para_editar = get_object_or_404(UnidadeMaterial, pk = idObjeto)
		formpost = FormUnidadeMaterial(request.POST, request.FILES, instance = unidadeMaterial_para_editar)
		formget = FormUnidadeMaterial(instance = unidadeMaterial_para_editar)	
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		centroCusto_para_editar = get_object_or_404(CentroCusto, pk = idObjeto)
		formpost = FormCentroCusto(request.POST, request.FILES, instance = centroCusto_para_editar)
		formget = FormCentroCusto(instance = centroCusto_para_editar)	
	if str(objeto) == 'fabricante':
		titulo = 'Fabricante'
		fabricante_para_editar = get_object_or_404(Fabricante, pk = idObjeto)
		formpost = FormFabricante(request.POST, request.FILES, instance = fabricante_para_editar)
		formget = FormFabricante(instance = fabricante_para_editar)
	if str(objeto) == 'material':
		titulo = 'Material'
		material_para_editar = get_object_or_404(Material, pk = idObjeto)
		formpost = FormMaterial(request.POST, request.FILES, instance = material_para_editar)
		formget = FormMaterial(instance = material_para_editar)
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = idObjeto)
		formpost = FormFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormFornecedor(instance = fornecedor_para_editar)
	if str(objeto) == 'gruposfornecedor':
		titulo = 'Grupos de Mercadoria'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = idObjeto)
		formpost = FormGruposFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormGruposFornecedor(instance = fornecedor_para_editar)
	if str(objeto) == 'requisicao':
		titulo = 'Requisicao'
		requisicao_para_editar = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		formpost = FormRequisicao(request.POST, request.FILES, instance = requisicao_para_editar)
		formget = FormRequisicao(instance = requisicao_para_editar)
	if str(objeto) == 'mapa':
		return HttpResponseRedirect("/finaliza/mapa/"+str(idObjeto))
	if str(objeto) == 'cotacao':
		titulo = 'Cotação'
		cotacao_para_editar = get_object_or_404(Cotacao, pk = idObjeto)
		if cotacao_para_editar.dtLimite < date.today():
			erro = 'A data limite para esta cotação foi: '
			data = cotacao_para_editar.dtLimite
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		formpost = FormCotacao(request.POST, request.FILES, instance = cotacao_para_editar)
		formget = FormCotacao(instance = cotacao_para_editar)
	if request.method == 'POST':
		form = formpost
		if form.is_valid():
			objeto_form = form.save(commit = False)
			if objeto_form.editar(request, idObjeto) != 'validos':
				erro =  objeto_form.editar(request, idObjeto)
				return render_to_response("edita.html", locals(), context_instance = RequestContext(request))
			if str(objeto) == 'gruposfornecedor':
				return HttpResponseRedirect("/lista/fornecedor")
			return HttpResponseRedirect("/lista/"+str(objeto))
		else:
			return render_to_response('edita.html', locals(), context_instance = RequestContext(request))	
	else:
		form = formget
	return render_to_response('edita.html', locals(), context_instance = RequestContext(request))

@login_required
def deleta(request, objeto, idObjeto):
	if not request.user.has_perm('interno.delete_'+str(objeto)):
			erro = 'Você não possui acesso para excluir '+str(objeto)
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(objeto) == 'grupomercadoria':
		objeto_para_deletar = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		form = FormGrupoMercadoria(instance = objeto_para_deletar)
	if str(objeto) == 'centrocusto':
		objeto_para_deletar = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormCentroCusto(instance = objeto_para_deletar)
	if str(objeto) == 'unidadematerial':
		objeto_para_deletar = get_object_or_404(UnidadeMaterial, pk = idObjeto)
		form = FormUnidadeMaterial(instance = objeto_para_deletar)
	if str(objeto) == 'fabricante':
		objeto_para_deletar = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormFabricante(instance = objeto_para_deletar)
	if str(objeto) == 'material':
		objeto_para_deletar = get_object_or_404(Material, pk = idObjeto)
		form = FormMaterial(instance = objeto_para_deletar)
	if str(objeto) == 'fornecedor':
		objeto_para_deletar = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormFornecedor(instance = objeto_para_deletar)
	if str(objeto) == 'requisicao':
		objeto_para_deletar = get_object_or_404(Requisicao, pk = idObjeto)
		form = FormRequisicao(instance = objeto_para_deletar)
	if str(objeto) == 'mapa':
		objeto_para_deletar = get_object_or_404(MapaComparativo, pk = idObjeto)
		form = FormMapaComparativo(instance = objeto_para_deletar)
	if request.method == 'POST':
		objeto_para_deletar.delete()
		return HttpResponseRedirect("/lista/"+str(objeto))
	else:
		return render_to_response('deleta.html', locals(), context_instance = RequestContext(request))

	
@login_required
def aprova(request, objeto, idObjeto):
	if str(objeto) == 'requisicao':
		titulo = 'Requisicao'
		titulo_membros = 'Itens da Requisicao'
		objeto = get_object_or_404(Requisicao, pk = idObjeto)
		itens = ItemRequisicao.objects.filter(requisicao = objeto)
		form = FormRequisicao(instance = objeto)
		if request.method == 'POST':
			if objeto.aprova() != 'Validos':
					erro =  objeto.aprova()
					return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))
			return HttpResponseRedirect("/lista/requisicao")
		else:
			return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))

@login_required
def filtra(request, objeto):
	if str(objeto) == 'material':
		titulo = 'Pesquisar Material'
		objetototal = 'Materiais'
		formpost = FormFiltraMaterial(request.POST, request.FILES)
		formget = FormFiltraMaterial()
		nomeMaterial = {'nomeMaterial': 'Nome do Material'}
		fabricante = {'fabricante': 'Fabricante'}
		grupoMercadoria = {'grupoMercadoria': 'Grupo de Mercadoria'}
		unidadeMaterial = {'unidadeMaterial': 'Unidade de Medida'}
		tpMaterial = {'tpMaterial': 'Tipo de Material'}
		campos = [nomeMaterial, fabricante, grupoMercadoria, unidadeMaterial, tpMaterial]
		colunas = ['Nome', 'Fabricante', 'Grupo de Mercadoria', 'Unidade de Medida', 'Tipo de Material']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valor_campo = []		
				for campo in campos:
					valor_campo.append(form.cleaned_data[campo.keys()[0]])
					if valor_campo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valor_campo[-1] == None:
						parametros.pop(-1)
				nomeMaterial = valor_campo[0]
				fabricante = valor_campo[1]
				grupoMercadoria = valor_campo[2]
				unidadeMaterial = valor_campo[3]
				tpMaterial = valor_campo[4]
				query = Material.objects.filter(nomeMaterial__icontains = nomeMaterial).filter(tpMaterial__icontains = tpMaterial)
				if fabricante != None:
					query = query.filter(fabricante = fabricante)
				if unidadeMaterial != None:
					query = query.filter(unidadeMaterial = unidadeMaterial)
				if grupoMercadoria != None:
					query = query.filter(grupoMercadoria = grupoMercadoria)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraMaterial()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(objeto) == 'fornecedor':
		titulo = 'Pesquisar Fornecedor'
		objetototal = 'Fornecedores'
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
				valor_campo = []		
				for campo in campos:
					valor_campo.append(form.cleaned_data[campo.keys()[0]])
					if valor_campo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valor_campo[-1] == None:
						parametros.pop(-1)
				razao = valor_campo[0]
				fantasia = valor_campo[1]
				cnpj = valor_campo[2]
				usuario = valor_campo[3]
				bairro = valor_campo[4]
				cidade = valor_campo[5]
				uf = valor_campo[6]
				status = valor_campo[7]
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

	if str(objeto) == 'mapa':
		titulo = 'Pesquisar Mapa Comparativo'
		objetototal = 'Mapas'
		formpost = FormFiltraMapaComparativo(request.POST, request.FILES)
		formget = FormFiltraMapaComparativo()
		dtLiberacaoP = {'dtLiberacaoP': 'Data de Liberação'}
		dtLiberacaoA = {'dtLiberacaoA': 'Data de Liberação'}
		fornecedor = {'fornecedorVencedor': 'Fornecedor'}
		status = {'status': 'Status'}
		campos = [dtLiberacaoP, dtLiberacaoA, fornecedor, status]
		colunas = ['Nº do Mapa', 'Data de Liberação', 'Fornecedor Vencedor', 'Item Cotado', 'Valor Cotado', 'Status do Mapa']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valor_campo = []		
				for campo in campos:
					valor_campo.append(form.cleaned_data[campo.keys()[0]])
					if valor_campo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valor_campo[-1] == None:
						parametros.pop(-1)
				dtLiberacaoP = valor_campo[0]
				dtLiberacaoA = valor_campo[1]
				fornecedor = valor_campo[2]
				status = valor_campo[3]
				query = MapaComparativo.objects.filter(status__icontains = status).order_by('id').reverse()
				requisicoes = Requisicao.objects.filter(solicitante = request.user)
				if requisicoes != None:
					itens = ItemRequisicao.objects.filter(requisicao__in = requisicoes)
					if itens != None:
						cotacoes = Cotacao.objects.filter(itemRequisicao__in = itens)
						if cotacoes != None:
							query = query.filter(cotacao__in = cotacoes)
				if dtLiberacaoP != None:
					query = query.filter(dtLiberacao__gte = dtLiberacaoP)
				if dtLiberacaoA != None:
					query = query.filter(dtLiberacao__lte = dtLiberacaoA)
				if fornecedor != None:
					cotacoes = Cotacao.objects.filter(fornecedor = fornecedor)
					query = query.filter(cotacaoVencedora__in = cotacoes)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraMapaComparativo()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(objeto) == 'cotacao':
		titulo = 'Pesquisar Cotação'
		objetototal = 'Cotações'
		formpost = FormFiltraCotacao(request.POST, request.FILES)
		formget = FormFiltraCotacao()
		dtLimiteP = {'dtLimiteP': 'Data Limite'}
		dtLimiteA = {'dtLimiteA': 'Data Limite'}
		vlCotacaoP = {'vlCotacaoP': 'Valor Cotado'}
		vlCotacaoA = {'vlCotacaoA': 'Valor Cotado'}
		itemRequisicao = {'itemRequisicao': 'Item Cotado'}
		campos = [dtLimiteP, dtLimiteA, vlCotacaoP, vlCotacaoA, itemRequisicao]
		colunas = ['Data Limite', 'Valor Cotado', 'Item da Cotação']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valor_campo = []		
				for campo in campos:
					valor_campo.append(form.cleaned_data[campo.keys()[0]])
					if valor_campo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valor_campo[-1] == None:
						parametros.pop(-1)
				dtLimiteP = valor_campo[0]
				dtLimiteA = valor_campo[1]
				vlCotacaoP = valor_campo[2]
				vlCotacaoA = valor_campo[3]
				itemRequisicao = valor_campo[4]
				fornecedor = Fornecedor.objects.filter(usuario = request.user)
				query = Cotacao.objects.filter(fornecedor = fornecedor).order_by('dtLimite').reverse()
				if dtLimiteP != None:
					query = query.filter(dtLimite__gte = dtLimiteP)
				if dtLimiteA != None:
					query = query.filter(dtLimite__lte = dtLimiteA)
				if vlCotacaoP != None:
					query = query.filter(vlCotacao__gte = vlCotacaoP)
				if vlCotacaoA != None:
					query = query.filter(vlCotacao__lte = vlCotacaoA)
				if itemRequisicao != None:
					query = query.filter(itemRequisicao = itemRequisicao)
				total = query.count()
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormFiltraCotacao()
		return render_to_response('pesquisa.html', locals(), context_instance = RequestContext(request))

	if str(objeto) == 'requisicao':
		titulo = 'Pesquisar Requisição'
		objetototal = 'Requisições'
		formpost = FormFiltraRequisicao(request.POST, request.FILES)
		formget = FormFiltraRequisicao()
		dtRequisicaoP = {'dtRequisicaoP': 'Data da Requisição'}
		dtRequisicaoA = {'dtRequisicaoA': 'Data de Requisição'}
		dtDeferimentoP = {'dtDeferimentoP': 'Data do Deferimento'}
		dtDeferimentoA = {'dtDeferimentoA': 'Data do Deferimento'}
		centroCusto = {'centroCusto': 'Centro de Custo'}
		itemRequisicao = {'itemRequisicao': 'Item'}
		status = {'status': 'Situação'}
		campos = [dtRequisicaoP, dtRequisicaoA, itemRequisicao, dtDeferimentoP, dtDeferimentoA, centroCusto, status]
		colunas = ['Nº Requisição', 'Data da Requisição', 'Solicitante', 'Data do Deferimento', 'Status']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				parametros = []	
				valor_campo = []		
				for campo in campos:
					valor_campo.append(form.cleaned_data[campo.keys()[0]])
					if valor_campo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valor_campo[-1] == None:
						parametros.pop(-1)
				dtRequisicaoP = valor_campo[0]
				dtRequisicaoA = valor_campo[1]
				itemRequisicao = valor_campo[2]
				dtDeferimentoP = valor_campo[3]
				dtDeferimentoA = valor_campo[4]
				centroCusto = valor_campo[5]
				status = valor_campo[6]
				query = Requisicao.objects.filter(status__icontains = status, solicitante = request.user).order_by('id').reverse()
				if dtRequisicaoP != None:
					query = query.filter(dtRequisicao__gte = dtRequisicaoP)
				if dtRequisicaoA != None:
					query = query.filter(dtRequisicao__lte = dtRequisicaoA)
				if dtDeferimentoP != None:
					query = query.filter(dtDeferimento__gte = dtDeferimentoP)
				if dtDeferimentoA != None:
					query = query.filter(dtDeferimento__lte = dtDeferimentoA)
				if centroCusto != None:
					query = query.filter(centroCusto = centroCusto)
				if itemRequisicao != None:
					itens = ItemRequisicao.objects.filter(requisicao__in = query, material = itemRequisicao)
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


@login_required
def finaliza(request, objeto, idObjeto):
	if str(objeto) == 'mapa':
		if not request.user.has_perm('interno.change_mapacomparativo'):
			erro = 'Você não possui acesso para finalizar mapa'
			return render_to_response("500.html", locals())
		titulo = 'Mapa Comparativo'
		objetototal = 'Cotações'
		formpost = FormMapaComparativo(request.POST, request.FILES)
		formget = FormMapaComparativo()
		erro = 'Mapa não existe'
		mapa = get_object_or_404(MapaComparativo, pk = idObjeto)
		if mapa.cotacao.all()[0].itemRequisicao.requisicao.solicitante != request.user:
			erro = 'Você só possui acesso aos mapas das suas requisições'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		if mapa.dtLiberacao >= date.today():
			erro = 'Mapa só estará liberado dia: '
			data = mapa.dtLiberacao + timedelta(1)
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		query = mapa.cotacao.all().order_by('vlCotacao')
		if request.method == 'POST':
			form = formpost
			if form.is_valid():	
				mapa.obs = form.cleaned_data['obs']
				if int(request.POST['cotacao']) != 0:
					id_cotacao = int(request.POST['cotacao'])
					mapa.cotacaoVencedora = Cotacao.objects.get(pk = id_cotacao)
				mapa.finaliza()	
				return HttpResponseRedirect("/lista/mapa")
			else:
				return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormMapaComparativo()
		return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))










