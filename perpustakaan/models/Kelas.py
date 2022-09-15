from odoo import api, fields, models


class Kelas(models.Model):
    _name = 'perpustakaan.kelas'
    _description = 'New Description'

    name = fields.Char(string='Nama Kelas')
    jurusan = fields.Char(string='Jurusan')
    fakultas = fields.Char(string='Fakultas')
    buku_id = fields.Many2many(comodel_name='perpustakaan.buku', string='Buku')
    