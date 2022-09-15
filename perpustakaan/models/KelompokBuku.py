from odoo import api, fields, models


class KelompokBuku(models.Model):
    _name = 'perpustakaan.kelompokbuku'
    _description = 'New Description'

    name = fields.Selection([
        ('teknologi', 'Teknologi'),
        ('bahasa', 'Bahasa'),
        ('sains dan matematika', 'Sains dan Matematika'),
        ('umum', 'Umum'),
        ('sejarah', 'Sejarah')
    ], string='Nama Kelompok')

    kode_kelompok = fields.Char(string='Kode Kelompok')

    @api.onchange('name')
    def _onchange_kode_kelompok(self):
        if self.name == 'teknologi':
            self.kode_kelompok = 'T01'
        elif self.name == 'bahasa':
            self.kode_kelompok = 'MAK02'
        elif self.name == 'sains dan matematika':
            self.kode_kelompok = 'SM01'
        elif self.name == 'umum':
            self.kode_kelompok = 'U01'
        elif self.name == 'sejarah':
            self.kode_kelompok = 'S01'

    kode_kelompok = fields.Char(string='Kode Kelompok Buku')
    kode_rak = fields.Char(string='Kode Rak')
    buku_ids = fields.One2many(comodel_name='perpustakaan.buku',
		                                inverse_name='kelompokbuku_id',
		                                string='Daftar Buku')
    jml_item = fields.Char(compute='_compute_jml_item', string='Jumlah Item')

    @api.depends('buku_ids')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['perpustakaan.buku'].search([('kelompokbuku_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_item = b
            record.daftar = a
    
    daftar = fields.Char(string='Daftar isi')