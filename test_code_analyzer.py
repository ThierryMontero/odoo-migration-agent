from agents.code_analyzer import CodeAnalyzer


def test_model_name_and_inherit():
    content = """
from odoo import models, fields


class SaleOrder(models.Model):
    _name = "custom.sale.order"
    _inherit = "sale.order"
    _description = "Custom Sale Order"
"""

    result = CodeAnalyzer().analyze(content)

    assert "custom.sale.order" in result["models"]
    assert "sale.order" in result["inherits"]
    assert "Custom Sale Order" in result["descriptions"]


def test_model_types():
    content = """
from odoo import models


class SaleOrder(models.Model):
    _name = "custom.sale.order"


class SaleWizard(models.TransientModel):
    _name = "custom.sale.wizard"


class SaleMixin(models.AbstractModel):
    _name = "custom.sale.mixin"
"""

    result = CodeAnalyzer().analyze(content)

    assert "models.Model" in result["model_types"]
    assert "models.TransientModel" in result["model_types"]
    assert "models.AbstractModel" in result["model_types"]


def test_simple_fields():
    content = """
from odoo import fields, models


class SaleOrder(models.Model):
    _name = "custom.sale.order"

    name = fields.Char()
    amount = fields.Float()
    active = fields.Boolean()
    date = fields.Date()
"""

    result = CodeAnalyzer().analyze(content)

    assert "name: Char" in result["fields"]
    assert "amount: Float" in result["fields"]
    assert "active: Boolean" in result["fields"]
    assert "date: Date" in result["fields"]


def test_relation_fields():
    content = """
from odoo import fields, models


class SaleOrder(models.Model):
    _name = "custom.sale.order"

    partner_id = fields.Many2one(
        "res.partner"
    )

    line_ids = fields.One2many(
        "custom.sale.order.line",
        "order_id"
    )

    tag_ids = fields.Many2many(
        "sale.order.tag"
    )
"""

    result = CodeAnalyzer().analyze(content)

    assert "partner_id: Many2one" in result["fields"]
    assert "line_ids: One2many" in result["fields"]
    assert "tag_ids: Many2many" in result["fields"]


def test_api_decorators():
    content = """
from odoo import api, models


class SaleOrder(models.Model):

    @api.depends("amount_total")
    def _compute_total(self):
        pass

    @api.onchange("partner_id")
    def _onchange_partner(self):
        pass

    @api.constrains("amount_total")
    def _check_amount(self):
        pass
"""

    result = CodeAnalyzer().analyze(content)

    assert "depends" in result["api_decorators"]
    assert "onchange" in result["api_decorators"]
    assert "constrains" in result["api_decorators"]

def test_methods():
    content = """
from odoo import models


class SaleOrder(models.Model):

    def _compute_custom_total(self):
        pass

    def action_confirm(self):
        pass

    def _onchange_partner(self):
        pass
"""

    result = CodeAnalyzer().analyze(content)

    assert "_compute_custom_total" in result["methods"]
    assert "action_confirm" in result["methods"]
    assert "_onchange_partner" in result["methods"]

def test_field_metadata():

    content = """
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_custom_total = fields.Float(
        string="Custom Total",
        compute="_compute_custom_total",
        store=True,
    )

    x_custom_reference = fields.Char(
        string="Reference",
        readonly=True,
    )

    def _compute_custom_total(self):
        pass
"""

    analyzer = CodeAnalyzer()

    result = analyzer.analyze(content)

    assert len(result["field_metadata"]) == 2

    custom_total = next(
        field
        for field in result["field_metadata"]
        if field["name"] == "x_custom_total"
    )

    assert custom_total["type"] == "Float"
    assert custom_total["compute"] == "_compute_custom_total"
    assert custom_total["store"] is True

    custom_reference = next(
        field
        for field in result["field_metadata"]
        if field["name"] == "x_custom_reference"
    )

    assert custom_reference["type"] == "Char"
    assert custom_reference["readonly"] is True
    assert custom_reference["compute"] is None