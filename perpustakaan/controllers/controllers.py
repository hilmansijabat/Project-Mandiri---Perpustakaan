# -*- coding: utf-8 -*-
# from odoo import http


# class Perpustakaan(http.Controller):
#     @http.route('/perpustakaan/perpustakaan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/perpustakaan/perpustakaan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('perpustakaan.listing', {
#             'root': '/perpustakaan/perpustakaan',
#             'objects': http.request.env['perpustakaan.perpustakaan'].search([]),
#         })

#     @http.route('/perpustakaan/perpustakaan/objects/<model("perpustakaan.perpustakaan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('perpustakaan.object', {
#             'object': obj
#         })

from crypt import methods
import json


import json

from odoo import http, models, fields
from odoo.http import request


class Perpustakaan(http.Controller):
    @http.route('/perpustakaan/getbuku', auth='public', method=['GET'])
    def getBuku(self, **kw):
        # Mengambil semua buku dari table buku
        buku = request.env['perpustakaan.buku'].search([])
        items = []

        for item in buku:
            items.append({
                'nama_buku': item.name,
                'harga_jual': item.harga_jual,
                'stok': item.stok
            })
        
        return json.dumps(items)

    @http.route('/perpustakaan/getkelas', auth='public', method=['GET'])
    def getSupplier(self, **kw):
        supplier = request.env['perpustakaan.kelas'].search([])
        items = []

        for item in supplier:
            items.append({
                'nama_kelas': item.name,
                'jurusan': item.jurusan,
                'fakultas': item.fakultas,
                'buku_id': item.buku_id[0].name
            })
        
        return json.dumps(items)