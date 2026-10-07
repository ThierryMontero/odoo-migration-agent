from odoo import fields, models


class CartinRefundWizard(models.TransientModel):

    _name = "cartin.refund.wizard"

    refund_id = fields.Many2one(
        "cartin.refund"
    )
