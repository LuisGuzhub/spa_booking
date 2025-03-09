# Define los metadatos del módulo y las dependencias necesarias.
{
    'name': 'SPA Booking Manager',  # Nombre del módulo
    'version': '1.0',   # Versión del módulo
    'summary': 'Module for managing SPA bookings and appointments', # Breve descripción
    'author': 'Luis chiquito',  # Autor del módulo
    'category': 'Services', # Categoría dentro de Odoo
    'depends': ['base', 'account'], # Dependencias del módulo (base y contabilidad)
    'data': ['security/ir.model.access.csv',    # Archivo de seguridad con permisos de acceso
             'views/spa_booking_views.xml',  # Definición de vistas del módulo
             'data/spa_booking_data.xml'],  # Datos de configuración inicial
    'assets': {
        'web.assets_backend': ['spa_booking/static/img/simboloPersona.png', ],  # Archivo de imagen
    },
    'installable': True,    # Indica que el módulo es instalable
    'application': True,    # Indica que el módulo se muestra como aplicación
}
