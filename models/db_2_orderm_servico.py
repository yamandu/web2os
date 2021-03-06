# -*- coding: utf-8 -*-

STATUS_OS = [(0, 'Aberta'), (1, 'Fechada'), (2, 'Cancelada')]

DEFAULT_REPRESENT = lambda value, row: value if value else ''

os_format = 'OS-%(id)06d'

db.define_table('ordem_servico',
                Field('cliente', db.cliente),
                Field('data_abertura', 'date', default=request.now),
                Field('total', 'double', default=0.0),
                Field('desconto', 'double', default=0.0, represent=DEFAULT_REPRESENT),
                Field('status', requires=IS_IN_SET(STATUS_OS), 
                      default=0, 
                      represent=lambda value, row: STATUS_OS[int(value)][1] if value else ''
                     ),
                format=os_format
               )
db.ordem_servico.id.represent = lambda value, row: os_format % row

db.define_table('ordem_servico_item',
                Field('ordem_servico', db.ordem_servico, writable=False, readable=False),
                Field('produto', db.produto),
                Field('quantidade', 'double', default=1),
                Field('valor_unitario', 'double', default=0.0),
                Field('total', compute=lambda row: row.quantidade * row.valor_unitario)
                )

db.define_table('ordem_servico_tarefa',
                Field('ordem_servico', db.ordem_servico, writable=False, readable=False),
                Field('servico', db.servico),
                Field('quantidade', 'integer', default=1),
                Field('valor_unitario', 'double', default=0.0),
                Field('total', compute=lambda row: row.quantidade * row.valor_unitario)
                )

def totaliza_os(os_id):

    soma_produto = db.ordem_servico_item.total.sum()
    total_produto = db(db.ordem_servico_item.ordem_servico == os_id).select(soma_produto).first()[soma_produto] or 0
    soma_servico = db.ordem_servico_tarefa.total.sum()
    total_servico = db(db.ordem_servico_tarefa.ordem_servico == os_id).select(soma_servico).first()[soma_servico] or 0
    desconto = db.ordem_servico[os_id].desconto or 0

    db(db.ordem_servico.id == os_id).update(total=total_produto + total_servico - desconto)
    
    db.commit()
