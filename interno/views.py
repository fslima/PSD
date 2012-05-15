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
		formpost = FormGrupoMercadoria(request.POST, request.FILES)
		formget = FormGrupoMercadoria()
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida do Material'
		formpost = FormUnidadeMedida(request.POST, request.FILES)
		formget = FormUnidadeMedida()	
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		formpost = FormCentroCusto(request.POST, request.FILES, )
		formget = FormCentroCusto()
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		formpost = FormFabricante(request.POST, request.FILES, )
		formget = FormFabricante()
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		formpost = FormMaterial(request.POST, request.FILES, )
		formget = FormMaterial()
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		formpost = FormFornecedor(request.POST, request.FILES, )
		formget = FormFornecedor()
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
	if str(tpObjeto) == 'mapa':
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
		lista = GrupoMercadoria.objects.filter(status = 'Ativo').order_by('nomeGrupoMercadoria')
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Cadastro de Unidades de Medida do Material'
		listaVazia = 'Nenhuma Unidade de Medida Cadastrada'
		lista = UnidadeMedida.objects.filter(status = 'Ativo').order_by('nomeUnidadeMedida')
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Cadastro de Centros de Custo'
		listaVazia = 'Nenhum Centro de Custo Cadastrado'
		lista = CentroCusto.objects.filter(status = 'Ativo').order_by('nomeCentroCusto')
	if str(tpObjeto) == 'fabricante':
		titulo = 'Cadastro de Fabricante'
		listaVazia = 'Nenhum Fabricante Cadastrado'
		lista = Fabricante.objects.filter(status = 'Ativo').order_by('nomeFabricante')
	if str(tpObjeto) == 'material':
		titulo = 'Cadastro de Materiais'
		listaVazia = 'Nenhum Material Cadastrado'
		lista = Material.objects.filter(status = 'Ativo').order_by('nomeMaterial')
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
	if str(tpObjeto) == 'mapa':
		titulo = 'Lista de Mapas Comparativos'
		listaVazia = 'Nenhum Mapa Cadastrado'
		lista = MapaComparativo.objects.filter(dtLiberacao__lt = datetime.now()).order_by('id').reverse()
		lista1 = []
		remover = []
		manter = []
		for mapa in lista:
			lista1.append(mapa)
			if mapa.cotacoes.all()[0].itemRequisicao.status == u'Mapa Finalizado' or mapa.cotacoes.all()[0].itemRequisicao.requisicao.solicitante != request.user:
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
		lista = Cotacao.objects.filter(fornecedor = fornecedor).exclude(dtLimite__lte = datetime.now() - timedelta(1)).order_by('id').reverse()
	if str(tpObjeto) == 'aprovacoes':
		titulo = 'Aprovações Pendentes'
		listaMapasVazia = 'Nenhum mapa pendente de aprovação'
		listaRequisicoesVazia = 'Nenhuma requisição pendente de aprovação'
		listaRequisicoes = Requisicao.objects.filter(status = u'Aguardando Aprovação').order_by('id').reverse()
		listaMapas = MapaComparativo.objects.filter(status = u'Aguardando Aprovação').order_by('id').reverse()
		return render_to_response('lista_aprovacoes.html', locals(), context_instance = RequestContext(request))
	return render_to_response('lista.html', locals(), context_instance = RequestContext(request))

def exibe(request, tpObjeto, idObjeto):
	if str(tpObjeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		objeto = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		form = FormGrupoMercadoria(instance = objeto)
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida'
		objeto = get_object_or_404(UnidadeMedida, pk = idObjeto)
		form = FormUnidadeMedida(instance = objeto)
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		objeto = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormCentroCusto(instance = objeto)
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		objeto = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormFabricante(instance = objeto)
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		objeto = get_object_or_404(Material, pk = idObjeto)
		v = vars(objeto)
		form = FormMaterial(instance = objeto)
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		objeto = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormFornecedor(instance = objeto)
	if str(tpObjeto) == 'requisicao':
		titulo = 'Requisicao'
		titulo_membros = 'Itens da Requisicao'
		objeto = get_object_or_404(Requisicao, pk = idObjeto, solicitante = request.user)
		itens = ItemRequisicao.objects.filter(requisicao = objeto)
		form = FormRequisicao(instance = objeto)
	if str(tpObjeto) == 'mapa':
		titulo = 'Mapa Comparativo'
		titulo_cotacoes = 'Cotacoes'
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		if objeto.dtLiberacao < date.today():
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
		grupoMercadoria_para_editar = get_object_or_404(GrupoMercadoria, pk = idObjeto)
		formpost = FormGrupoMercadoria(request.POST, request.FILES, instance = grupoMercadoria_para_editar)
		formget = FormGrupoMercadoria(instance = grupoMercadoria_para_editar)
		titulo = 'Grupo de Mercadoria'		
	if str(tpObjeto) == 'unidademedida':
		titulo = 'Unidade de Medida'
		unidadeMedida_para_editar = get_object_or_404(UnidadeMedida, pk = idObjeto)
		formpost = FormUnidadeMedida(request.POST, request.FILES, instance = unidadeMedida_para_editar)
		formget = FormUnidadeMedida(instance = unidadeMedida_para_editar)	
	if str(tpObjeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		centroCusto_para_editar = get_object_or_404(CentroCusto, pk = idObjeto)
		formpost = FormCentroCusto(request.POST, request.FILES, instance = centroCusto_para_editar)
		formget = FormCentroCusto(instance = centroCusto_para_editar)	
	if str(tpObjeto) == 'fabricante':
		titulo = 'Fabricante'
		fabricante_para_editar = get_object_or_404(Fabricante, pk = idObjeto)
		formpost = FormFabricante(request.POST, request.FILES, instance = fabricante_para_editar)
		formget = FormFabricante(instance = fabricante_para_editar)
	if str(tpObjeto) == 'material':
		titulo = 'Material'
		material_para_editar = get_object_or_404(Material, pk = idObjeto)
		formpost = FormMaterial(request.POST, request.FILES, instance = material_para_editar)
		formget = FormMaterial(instance = material_para_editar)
	if str(tpObjeto) == 'fornecedor':
		titulo = 'Fornecedor'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = idObjeto)
		formpost = FormFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormFornecedor(instance = fornecedor_para_editar)
	if str(tpObjeto) == 'gruposfornecedor':
		tpObjeto = 'fornecedor'
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
	if str(tpObjeto) == 'mapa':
		return HttpResponseRedirect("/finaliza/mapa/"+str(idObjeto))
	if str(tpObjeto) == 'cotacao':
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
		form = FormGrupoMercadoria(instance = objeto_para_deletar)
	if str(tpObjeto) == 'centrocusto':
		objeto_para_deletar = get_object_or_404(CentroCusto, pk = idObjeto)
		form = FormCentroCusto(instance = objeto_para_deletar)
	if str(tpObjeto) == 'unidademedida':
		objeto_para_deletar = get_object_or_404(UnidadeMedida, pk = idObjeto)
		form = FormUnidadeMedida(instance = objeto_para_deletar)
	if str(tpObjeto) == 'fabricante':
		objeto_para_deletar = get_object_or_404(Fabricante, pk = idObjeto)
		form = FormFabricante(instance = objeto_para_deletar)
	if str(tpObjeto) == 'material':
		objeto_para_deletar = get_object_or_404(Material, pk = idObjeto)
		form = FormMaterial(instance = objeto_para_deletar)
	if str(tpObjeto) == 'fornecedor':
		objeto_para_deletar = get_object_or_404(Fornecedor, pk = idObjeto)
		form = FormFornecedor(instance = objeto_para_deletar)
	if str(tpObjeto) == 'requisicao':
		objeto_para_deletar = get_object_or_404(Requisicao, pk = idObjeto)
		if objeto_para_deletar.status == u'Aprovada':
			erro = 'Não é possível alterar requisição já aprovada'
			return render_to_response("500.html", locals(), context_instance = RequestContext(request))
		form = FormRequisicao(instance = objeto_para_deletar)
	if str(tpObjeto) == 'mapa':
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
	if str(tpObjeto) == 'requisicao':
		titulo = 'Aprovar Requisição: '
		objeto = get_object_or_404(Requisicao, pk = idObjeto)
		itens = ItemRequisicao.objects.filter(requisicao = idObjeto)
		form = FormRequisicao(instance = objeto)
	if str(tpObjeto) == 'mapa':
		titulo = 'Aprovar Mapa: '
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		cotacoes = objeto.cotacoes.all().order_by('vlCotacao')
		form = FormExibeMapaComparativo(instance = objeto)
	if request.method == 'POST':
		if objeto.aprovar() != 'Validos':
			erro =  objeto.aprovar()
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
	if str(tpObjeto) == 'mapa':
		titulo = 'Reprovar Mapa: '
		objeto = get_object_or_404(MapaComparativo, pk = idObjeto)
		cotacoes = objeto.cotacoes.all().order_by('vlCotacao')
		form = FormExibeMapaComparativo(instance = objeto)

	if objeto.reprovar() != 'Validos':
		erro =  objeto.aprovar()
		return render_to_response('aprova.html', locals(), context_instance = RequestContext(request))
	return HttpResponseRedirect("/lista/aprovacoes")
	
@login_required
def filtra(request, tpObjeto):
	if str(tpObjeto) == 'material':
		titulo = 'Pesquisar Material'
		radicalObjeto = 'Materia'
		formpost = FormFiltraMaterial(request.POST, request.FILES)
		formget = FormFiltraMaterial()
		nomeMaterial = {'nomeMaterial': 'Nome do Material'}
		fabricante = {'fabricante': 'Fabricante'}
		grupoMercadoria = {'grupoMercadoria': 'Grupo de Mercadoria'}
		unidadeMedida = {'unidadeMedida': 'Unidade de Medida'}
		tpMaterial = {'tpMaterial': 'Tipo de Material'}
		status = {'status': 'Situação'}
		campos = [nomeMaterial, fabricante, grupoMercadoria, unidadeMedida, tpMaterial, status]
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
				nomeMaterial = valorCampo[0]
				fabricante = valorCampo[1]
				grupoMercadoria = valorCampo[2]
				unidadeMedida = valorCampo[3]
				tpMaterial = valorCampo[4]
				status = valorCampo[5]
				query = Material.objects.filter(nomeMaterial__icontains = nomeMaterial).filter(tpMaterial__icontains = tpMaterial)
				if fabricante != None:
					query = query.filter(fabricante = fabricante)
				if unidadeMedida != None:
					query = query.filter(unidadeMedida = unidadeMedida)
				if grupoMercadoria != None:
					query = query.filter(grupoMercadoria = grupoMercadoria)
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

	if str(tpObjeto) == 'mapa':
		titulo = 'Pesquisar Mapa Comparativo'
		radicalObjeto = 'Mapa'
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
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dtLiberacaoP = valorCampo[0]
				dtLiberacaoA = valorCampo[1]
				fornecedor = valorCampo[2]
				status = valorCampo[3]
				query = MapaComparativo.objects.all().order_by('id').reverse()
				requisicoes = Requisicao.objects.filter(solicitante = request.user)
				if requisicoes != None:
					itens = ItemRequisicao.objects.filter(requisicao__in = requisicoes)
					if itens != None:
						cotacoes = Cotacao.objects.filter(itemRequisicao__in = itens)
						if cotacoes != None:
							query = query.filter(cotacoes__in = cotacoes).distinct('id')
				if dtLiberacaoP != None:
					query = query.filter(dtLiberacao__gte = dtLiberacaoP)
				if dtLiberacaoA != None:
					query = query.filter(dtLiberacao__lte = dtLiberacaoA)
				if status != '':
					query = query.filter(status = status)
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

	if str(tpObjeto) == 'cotacao':
		titulo = 'Pesquisar Cotação'
		radicalObjeto = 'Cotaç'
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
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dtLimiteP = valorCampo[0]
				dtLimiteA = valorCampo[1]
				vlCotacaoP = valorCampo[2]
				vlCotacaoA = valorCampo[3]
				itemRequisicao = valorCampo[4]
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
					itens = ItemRequisicao.objects.filter(material = itemRequisicao)
					query = query.filter(itemRequisicao__in = itens)
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
				valorCampo = []		
				for campo in campos:
					valorCampo.append(form.cleaned_data[campo.keys()[0]])
					if valorCampo[-1] != '':
						parametros.append(campo[campo.keys()[0]])
					if valorCampo[-1] == None:
						parametros.pop(-1)
				dtRequisicaoP = valorCampo[0]
				dtRequisicaoA = valorCampo[1]
				itemRequisicao = valorCampo[2]
				dtDeferimentoP = valorCampo[3]
				dtDeferimentoA = valorCampo[4]
				centroCusto = valorCampo[5]
				status = valorCampo[6]
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

	if str(tpObjeto) == 'fabricante':
		titulo = 'Pesquisar Fabricante'
		radicalObjeto = 'Fabricante'
		formpost = FormFiltraFabricante(request.POST, request.FILES)
		formget = FormFiltraFabricante()
		nomeFabricante = {'nomeFabricante': 'Nome do Fabricante'}
		status = {'status': 'Situação'}
		campos = [nomeFabricante, status]
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
				nomeFabricante = valorCampo[0]
				status = valorCampo[1]
				query = Fabricante.objects.filter(nomeFabricante__icontains = nomeFabricante).order_by('nomeFabricante')
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
		nomeUnidadeMedida = {'nomeUnidadeMedida': 'Unidade de Medida'}
		descUnidadeMedida = {'descUnidadeMedida': 'Descrição'}
		status = {'status': 'Situação'}
		campos = [nomeUnidadeMedida, descUnidadeMedida, status]
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
				nomeUnidadeMedida = valorCampo[0]
				descUnidadeMedida = valorCampo[1]
				status = valorCampo[2]
				query = UnidadeMedida.objects.filter(nomeUnidadeMedida__icontains = nomeUnidadeMedida).filter(nomeUnidadeMedida__icontains = nomeUnidadeMedida).order_by('descUnidadeMedida')
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
		nomeGrupoMercadoria = {'nomeGrupoMercadoria': 'Grupo de Mercadoria'}
		status = {'status': 'Situação'}
		campos = [nomeGrupoMercadoria, status]
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
				nomeGrupoMercadoria = valorCampo[0]
				status = valorCampo[1]
				query = GrupoMercadoria.objects.filter(nomeGrupoMercadoria__icontains = nomeGrupoMercadoria).order_by('nomeGrupoMercadoria')
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
		nomeCentroCusto = {'nomeCentroCusto': 'Centro de Custo'}
		gerente = {'gerente': 'Gerente'}
		status = {'status': 'Situação'}
		campos = [nomeCentroCusto, gerente, status]
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
				nomeCentroCusto = valorCampo[0]
				gerente = valorCampo[1]
				status = valorCampo[2]
				query = CentroCusto.objects.filter(nomeCentroCusto__icontains = nomeCentroCusto).order_by('nomeCentroCusto')
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
	if str(tpObjeto) == 'mapa':
		if not request.user.has_perm('interno.change_mapacomparativo'):
			erro = 'Você não possui acesso para finalizar mapa'
			return render_to_response("500.html", locals())
		titulo = 'Mapa Comparativo'
		objetototal = 'Cotações'
		formpost = FormMapaComparativo(request.POST, request.FILES)
		formget = FormMapaComparativo()
		erro = 'Mapa não existe'
		mapa = get_object_or_404(MapaComparativo, pk = idObjeto)
		if mapa.cotacoes.all()[0].itemRequisicao.requisicao.solicitante != request.user:
			erro = 'Você só possui acesso aos mapas das suas requisições'
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		if mapa.dtLiberacao >= date.today():
			erro = 'Mapa só estará liberado dia: '
			data = mapa.dtLiberacao + timedelta(1)
			return render_to_response('500.html', locals(), context_instance = RequestContext(request))
		query = mapa.cotacoes.all().order_by('vlCotacao')
		if request.method == 'POST':
			form = formpost
			if form.is_valid():	
				mapa.obs = form.cleaned_data['obs']
				if int(request.POST['cotacao']) != 0:
					id_cotacao = int(request.POST['cotacao'])
					mapa.cotacaoVencedora = Cotacao.objects.get(pk = id_cotacao)
				else:
					mapa.cotacaoVencedora = None
				mapa.finalizar()	
				return HttpResponseRedirect("/lista/mapa")
			else:
				return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormMapaComparativo(instance = mapa)
		return render_to_response('finaliza.html', locals(), context_instance = RequestContext(request))










