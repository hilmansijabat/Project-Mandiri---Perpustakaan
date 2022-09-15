from odoo import api, fields, models


'''
Membuat model BukuDatang yang inherit
ke Transient Model
'''
class BukuDatang(models.TransientModel):
    _name = 'perpustakaan.bukudatang'

    buku_id = fields.Many2one(comodel_name='perpustakaan.buku', string='Nama Buku', required=True)
    jumlah = fields.Integer(string='Jumlah', required=False)

    def button_buku_datang(self):
        for line in self:
            self.env['perpustakaan.buku'].search([('id', '=', line.buku_id.id)]).write(
                {'stok': line.buku_id.stok +  line.jumlah}
            )