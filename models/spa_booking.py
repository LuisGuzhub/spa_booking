from odoo import models, fields, api

# Modelo principal para la gestión de reservas del SPA
class SpaBooking(models.Model):
    _name = 'spa.booking'   # Nombre técnico del modelo
    _description = 'SPA Booking Management' # Descripción del modelo
    _rec_name = 'name'  # Define qué campo se mostrará como nombre del registro en las vistas

    # Datos principales de la reserva
    name = fields.Char(string='Client', required=True, store=True)
    phone = fields.Char(string="Phone", store=True)
    appointment_date = fields.Datetime(string="Date and Time", required=True, store=True)
    email = fields.Char(string="Email", store=True)
    address = fields.Char(string="Address", store=True)
    custom_type = fields.Selection([
        ('new', 'New'),
        ('recurring', 'Recurring'),
        ('vip', 'VIP'),
    ], string='Customer Type', default='new', store=True)   # Identifica si el cliente es nuevo, recurrente o VIP

    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ], default='pending', string="Status", store=True)  # Estado de la reserva (pendiente, confirmada o cancelada)

    service_option = fields.Many2one(
        'spa.category',
        string="Service Options",
        required=True,
        ondelete='cascade'  # Si se elimina la categoría, se eliminan las reservas asociadas
    )

    detail_ids = fields.One2many('spa.detail', 'booking_id', string="Booking Details")
    # Imagen del cliente (opcional)
    image = fields.Image(string="Image")

    # Relación con la factura generada en Odoo
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True, copy=False)

    # Booleano que indica si se debe mostrar el botón de ver factura
    show_invoice = fields.Boolean(compute="_compute_show_invoice")

    @api.depends('invoice_id')
    def _compute_show_invoice(self):
        """Actualiza el estado de visibilidad del botón 'Ver Factura'"""
        for record in self:
            record.show_invoice = bool(record.invoice_id)

    def action_view_invoice(self):
        """Abre la factura generada para la reserva"""
        self.ensure_one()
        if self.invoice_id:
            return {
                'name': "Invoice",
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id,
                'target': 'current',
            }

    def action_generate_invoice(self):
        """Generar una factura cuando la reserva es confirmada"""
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)  # Busca un diario contable de ventas
        partner = self.env['res.partner'].search([('name', '=', self.name)], limit=1)   # Busca si el cliente ya existe

        if not partner:
            partner = self.env['res.partner'].create({'name': self.name})   # Si no existe, lo crea

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice', # Indica que es una factura de venta
            'partner_id': partner.id,   # Cliente vinculado a la factur
            'invoice_date': fields.Date.today(),    # Fecha de emisión
            'journal_id': journal.id,   # Diario contable asociado
            'invoice_line_ids': [(0, 0, {
                'name': f"SPA Services - {self.name}",  # Descripción de la factura
                'quantity': 1,  # Cantidad de servicios
                'price_unit': sum(self.detail_ids.mapped('price')), # Suma total de los servicios reservados
                'account_id': journal.default_account_id.id,    # Cuenta contable predeterminada
            })],
        })
        self.invoice_id = invoice.id    # Asigna la factura al registro de la reserva
        return self.action_view_invoice()   # Abre la factura generada

    def action_confirm_booking(self):
        """Confirma la reserva y genera la factura"""
        self.write({'status': 'confirmed'}) # Cambia el estado a 'confirmed'
        return self.action_generate_invoice()   # Genera la factura automáticamente

# Modelo para los detalles de la reserva (servicios seleccionados)
class SpaDetail(models.Model):
    _name = 'spa.detail'    # Nombre técnico del modelo
    _description = 'Booking Details'    # Descripción del modelo

    booking_id = fields.Many2one('spa.booking', string="Booking", required=True)    # Relación con la reserva
    service_id = fields.Many2one(
        'spa.service',
        string="Service",
        required=True,
        domain="[('category_id', '=', parent.service_option)]"  # Restringe los servicios según la categoría elegida
    )
    price = fields.Float(string="Price", related='service_id.price', store=True)    # Obtiene el precio del servicio seleccionado
