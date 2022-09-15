from odoo import api, fields, models


class Person(models.Model):
    _name = 'perpustakaan.person'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    nip = fields.Char(string='NIP')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')


class KepalaPerpustakaan(models.Model):
    _name = 'perpustakaan.kepalaperpustakaan'
    _inherit = 'perpustakaan.person'
    _description = 'New Description'

    id_kepalaperpustakaan = fields.Char(string='ID Kepala Perpustakaan')


class Pustakawan(models.Model):
    _name = 'perpustakaan.pustakawan'
    _inherit = 'perpustakaan.person'
    _description = 'New Description'

    id_cln = fields.Char(string='ID Pustakawan')