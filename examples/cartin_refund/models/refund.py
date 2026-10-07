from odoo import api, fields, models


class CartinRefund(models.Model):

    _name = "cartin.refund"
    _description = "Cartin Refund"

    name = fields.Char(
        required=True
    )

    amount = fields.Float()

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Done"),
        ],
        default="draft",
    )

    @api.model
    def create_refund(self, name, amount):
        return self.create({
            "name": name,
            "amount": amount,
        })