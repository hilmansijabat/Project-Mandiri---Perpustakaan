from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Peminjaman(models.Model):
    _name = 'perpustakaan.peminjaman'
    _description = 'Peminjaman'

    name = fields.Char(string='No. Peminjaman')
    nama_peminjam = fields.Char(string='Nama Peminjam')
    tgl_peminjaman = fields.Datetime(
        string='Tanggal Peminjaman',
        default=fields.Datetime.now())
    total_satuan = fields.Integer(
        string='Jumlah Buku Pinjaman',
        compute='_compute_totalbuku')
    detailpeminjaman_ids = fields.One2many(
        comodel_name='perpustakaan.detailpeminjaman',
        inverse_name='peminjaman_id',
        string='Detail Peminjaman')

    @api.depends('detailpeminjaman_ids')
    def _compute_totalbuku(self):
        for line in self:
            result = sum(self.env['perpustakaan.detailpeminjaman'].search(
                [('peminjaman_id', '=', line.id)]).mapped('subtotal'))
            line.total_satuan = result


class DetailPeminjaman(models.Model):
    _name = 'perpustakaan.detailpeminjaman'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    peminjaman_id = fields.Many2one(
        comodel_name='perpustakaan.peminjaman',
        string='Detail Peminjaman')
    buku_id = fields.Many2one(
        comodel_name='perpustakaan.buku',
        string='List Buku')
    total_satuan = fields.Integer(
        string='Total Satuan',
        onchange='_onchange_buku_id')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    def write(self, vals):
      for line in self:
          data_asli = self.env['perpustakaan.detailpeminjaman'].search([('peminjaman_id', '=', line.id)])
          print(data_asli)

          for data in data_asli:
              print(str(data.buku_id.name) + " " + str(data.qty) + ' ' + str(data.buku_id.stok))
              data.buku_id.stok += data.qty
      
      line = super(Peminjaman, self).write(vals)
      
      for line in self:
          data_setelah_edit = self.env['perpustakaan.detailpeminjaman'].search([('peminjaman_id', '=', line.id)])
          print(data_asli)
          print(data_setelah_edit)

          for data_baru in data_setelah_edit:
              if data_baru in data_asli:
                  print(data_baru.buku_id.name + " " + str(data_baru.qty) + ' ' + str(data_baru.buku_id.stok))
                  data_baru.buku_id.stok -= data_baru.qty
              else:
                  pass

      return line

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah peminjaman harus minimal 1, silahkan input dengan benar!')
            elif line.buku_id.stok < line.qty:
                raise ValidationError('Stok yang tersedia tidak mencukupi.')

    @api.depends('total_satuan', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.total_satuan

    @api.onchange('buku_id')
    def _onchange_buku_id(self):
        if self.buku_id.total_jumlah:
            self.total_satuan = self.buku_id.total_jumlah

    @api.model
    def create(self, vals):
        line = super(DetailPeminjaman, self).create(vals)
        if line.qty:
            # Mendapatkan data berdasarkan ID pada buku_id
            self.env['perpustakaan.buku'].search(
                [('id', '=', line.buku_id.id)]
            ).write({'stok': line.buku_id.stok - line.qty})

        return line

    @api.ondelete(at_uninstall=False)
    def __ondelete_peminjaman(self):
        if self.detailpeminjaman_ids:
            peminjaman = []
            for line in self:
                peminjaman = self.env['perpustakaan.detailpeminjaman'].search(
                    [('peminjaman_id', '=', line.id)])
                print(peminjaman)

            for ob in peminjaman:
                print(ob.buku_id.name + ' ' + str(ob.qty))
                ob.buku_id.stok += ob.qty

    def unlink(self):
        if self.detailpeminjaman_ids:
            peminjaman = []
            for line in self:
                peminjaman = self.env['perpustakaan.detailpeminjaman'].search(
                    [('peminjaman_id', '=', line.id)])
                print(peminjaman)

            for ob in peminjaman:
                print(ob.buku_id.name + ' ' + str(ob.qty))
                ob.buku_id.stok += ob.qty

        line = super(Peminjaman, self).unlink()

    sql_constraints = [
        ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
    ]

    