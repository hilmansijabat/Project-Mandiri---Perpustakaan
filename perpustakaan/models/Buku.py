from odoo import api, fields, models


class Buku(models.Model):
    _name = 'perpustakaan.buku'
    _description = 'New Description'

    name = fields.Char(string='Nama Buku', required=True)
    penerbit = fields.Char(string='Penerbit', required=True)
    tahun_terbit = fields.Char(string='Tahun Terbit', required=True)

    kelompokbuku_id = fields.Many2one(comodel_name='perpustakaan.kelompokbuku',
    string='Kelompok Buku', ondelete='cascade')

    kelas_id = fields.Many2many(comodel_name='perpustakaan.kelas', string='Kelas')

    stok = fields.Integer(string='Stok')