# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    links = [lambda row: A('Editar', _href=URL(f='editar_os', vars={'os_id': row.id}))]
    return dict(grid=SQLFORM.grid(db.ordem_servico, create=False, editable=False, details=False, links=links))

@auth.requires_login()
def nova_os():
    form = SQLFORM(db.ordem_servico, fields=['cliente']).process()
    if form.accepted:
        redirect(URL(f='editar_os', vars={'os_id': form.vars.id}))

    return dict(form=form)


@auth.requires_login()
def editar_os():
    os_id = request.vars.os_id

    db.ordem_servico.cliente.writable = False
    db.ordem_servico.data_abertura.writable = False
    db.ordem_servico.total.writable = False

    form = SQLFORM(db.ordem_servico, os_id, submit_button='Salvar').process()

    if form.accepted:
        totaliza_os(os_id)
        form = SQLFORM(db.ordem_servico, os_id, submit_button='Salvar').process()

    db.ordem_servico_item.id.represent = lambda v, r: CAT(v,
                                                          A('Excluir', 
                                                            _href=URL(f='excluir_item',
                                                                      vars={'id': v, 'os_id': os_id}),
                                                            _onclick='return confirm("Excluir?");'
                                                           ))
    items = db(db.ordem_servico_item.ordem_servico == os_id).select()

    db.ordem_servico_tarefa.id.represent = lambda v, r: CAT(v,
                                                          A('Excluir', 
                                                            _href=URL(f='excluir_servico',
                                                                      vars={'id': v, 'os_id': os_id}),
                                                            _onclick='return confirm("Excluir?");'
                                                            ))
    servicos = db(db.ordem_servico_tarefa.ordem_servico == os_id).select()

    return dict(form=form, items=items, servicos=servicos)


@auth.requires_login()
def inserir_item():
    os_id = request.vars.os_id
    
    db.ordem_servico_item.ordem_servico.default = os_id
    db.ordem_servico_item.ordem_servico.writable = False
    db.ordem_servico_item.ordem_servico.readable = False
    form = SQLFORM(db.ordem_servico_item).process()
    
    if form.accepted: 
        totaliza_os(os_id)
        redirect(URL(f='editar_os', vars=request.vars))
    
    return dict(form=form)


@auth.requires_login()
def inserir_servico():
    os_id = request.vars.os_id

    db.ordem_servico_tarefa.ordem_servico.default = os_id
    db.ordem_servico_tarefa.ordem_servico.writable = False
    db.ordem_servico_tarefa.ordem_servico.readable = False
    form = SQLFORM(db.ordem_servico_tarefa).process()

    if form.accepted: 
        totaliza_os(os_id)
        redirect(URL(f='editar_os', vars=request.vars))

    return dict(form=form)


@auth.requires_login()
def excluir_item():
    del db.ordem_servico_item[request.vars.id]
    totaliza_os(request.vars.os_id)
    redirect(URL(f='editar_os', vars={'os_id': request.vars.os_id}))

@auth.requires_login()
def excluir_servico():
    del db.ordem_servico_tarefa[request.vars.id]
    totaliza_os(request.vars.os_id)
    redirect(URL(f='editar_os', vars={'os_id': request.vars.os_id}))
