from odoo import models, fields


class MyModel(models.Model):
    _name = "my.model"

    name = fields.Char(required=True)
