from pathlib import Path

from agents.custom_code_analyzer import CustomCodeAnalyzer



def create_module(tmp_path: Path):
    module = tmp_path / "test_module"
    module.mkdir()

    (module / "__manifest__.py").write_text(
        """
{
    "name": "Test Module",
    "version": "16.0.1.0.0",
    "depends": ["sale"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
""",
        encoding="utf-8",
    )

    models = module / "models"
    models.mkdir()

    (models / "sale_order.py").write_text(
        """
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_custom_total = fields.Float(
        string="Custom Total"
    )

    @api.depends("amount_total")
    def _compute_custom_total(self):
        for record in self:
            record.x_custom_total = record.amount_total
""",
        encoding="utf-8",
    )

    views = module / "views"
    views.mkdir()

    (views / "sale_order_views.xml").write_text(
        """
<odoo>

    <record id="view_sale_order_custom" model="ir.ui.view">
        <field name="name">sale.order.custom</field>
        <field name="model">sale.order</field>
        <field name="arch" type="xml">
            <form>
                <field name="x_custom_total"/>
                <field name="amount_total"/>
            </form>
        </field>
    </record>

    <record id="action_sale_order_custom"
            model="ir.actions.act_window">
        <field name="name">Sale Orders</field>
        <field name="res_model">sale.order</field>
    </record>

    <menuitem
        id="menu_sale_order_custom"
        name="Custom Sales"
    />

</odoo>
""",
        encoding="utf-8",
    )

    return module


def test_custom_code_analyzer(tmp_path):
    module = create_module(tmp_path)

    analyzer = CustomCodeAnalyzer()

    result = analyzer.analyze(str(module))

    assert result["module"] == str(module)

    assert result["manifest"]["name"] == "Test Module"

    assert len(result["python"]) == 1

    python = result["python"][0]

    assert "SaleOrder" in python["classes"]
    assert "sale.order" in python["inherits"]
    assert "x_custom_total: Float" in python["fields"]
    assert "depends" in python["api_decorators"]

    assert len(result["xml"]) == 1

    xml = result["xml"][0]

    assert len(xml["views"]) == 1
    assert xml["views"][0]["model"] == "sale.order"

    assert "x_custom_total" in xml["views"][0]["fields"]

    assert "action_sale_order_custom" in xml["actions"]

    assert len(xml["menus"]) == 1
    assert xml["menus"][0]["id"] == "menu_sale_order_custom"

def test_custom_code_analyzer_includes_functional_analysis(tmp_path):

    module = create_module(tmp_path)

    analyzer = CustomCodeAnalyzer()

    result = analyzer.analyze(str(module))

    assert "functional" in result

    functional = result["functional"]

    assert functional["type"] == "functional_analysis"

    assert functional["model"] == "sale.order"

    assert "x_custom_total" in functional["custom_behavior"]

    assert "_compute_custom_total" in functional["custom_behavior"]

    assert "view_sale_order_custom" in functional["custom_behavior"]

    assert functional["technical_elements"]["fields"] == [
        "x_custom_total: Float"
    ]

    assert functional["technical_elements"]["methods"] == [
        "_compute_custom_total"
    ]

    assert len(functional["technical_elements"]["xpaths"]) == 0

def test_custom_code_analyzer_aggregates_multiple_python_files(tmp_path):

    module = create_module(tmp_path)

    models = module / "models"

    (models / "account_move.py").write_text(
        """
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    x_custom_reference = fields.Char()

    def action_custom_reference(self):
        pass
""",
        encoding="utf-8",
    )

    analyzer = CustomCodeAnalyzer()

    result = analyzer.analyze(str(module))

    assert len(result["python"]) == 2

    functional = result["functional"]

    assert "x_custom_total" in functional["custom_behavior"]
    assert "x_custom_reference" in functional["custom_behavior"]

    assert "_compute_custom_total" in functional["custom_behavior"]
    assert "action_custom_reference" in functional["custom_behavior"]

    assert "x_custom_total: Float" in (
        functional["technical_elements"]["fields"]
    )

    assert "x_custom_reference: Char" in (
        functional["technical_elements"]["fields"]
    )


