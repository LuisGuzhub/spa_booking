# Modelo que representa los servicios del SPA.
from odoo import models, fields, api


class SpaService(models.Model):
    _name = 'spa.service'  # Nombre técnico del modelo
    _description = 'SPA Services'  # Descripción del modelo
    _rec_name = 'name'  # Especifica qué campo se usará como nombre visible en listas

    # Campos del modelo
    name = fields.Char(string="Service Name", required=True)  # Nombre del servicio
    price = fields.Float(string="Price", required=True)  # Precio del servicio
    category_id = fields.Many2one('spa.category', string="Category", required=True)

    # Relación Many2one con 'spa.category', que indica a qué categoría pertenece el servicio

    @api.model
    def name_get(self):
        """
        Sobreescribe la función name_get para modificar cómo se muestra el nombre del servicio
        en las listas desplegables de Odoo. En lugar de solo el ID, muestra el nombre del servicio.
        """
        result = []
        for service in self:
            result.append((service.id, service.name))   # Guarda una tupla con el ID y el nombre del servicio
        return result   # Retorna la lista de servicios con su ID y nombre
