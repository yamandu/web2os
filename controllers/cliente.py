# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    return dict(grid=SQLFORM.grid(db.cliente))
