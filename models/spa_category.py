# Modelo que define las categorías de los servicios.
from odoo import models, fields, api

class SpaCategory(models.Model):
    _name = 'spa.category'  # Nombre técnico del modelo
    _description = 'Service Category'   # Descripción del modelo

    name = fields.Char(string="Name", required=True)    # Nombre de la categoría
    description = fields.Text(string="Description")     # Descripción de la categoría
    service_ids = fields.One2many('spa.service', 'category_id', string="Services")     # Relación con los servicios
