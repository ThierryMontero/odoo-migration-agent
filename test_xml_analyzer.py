from agents.xml_analyzer import XMLAnalyzer


def test_xpath_in_view(tmp_path):
    xml_file = tmp_path / "sale_order_view.xml"

    xml_file.write_text(
        """
<odoo>

    <record id="view_sale_order_custom" model="ir.ui.view">

        <field name="name">
            sale.order.custom
        </field>

        <field name="model">
            sale.order
        </field>

        <field name="inherit_id"
               ref="sale.view_order_form"/>

        <field name="arch" type="xml">

            <xpath expr="//field[@name='amount_total']"
                   position="after">

                <field name="x_custom_total"/>

            </xpath>

        </field>

    </record>

</odoo>
""",
        encoding="utf-8",
    )

    result = XMLAnalyzer().analyze(
        str(xml_file)
    )

    assert len(result["views"]) == 1

    view = result["views"][0]

    assert view["model"] == "sale.order"

    assert "x_custom_total" in view["fields"]


def test_xpath_metadata(tmp_path):
    xml_file = tmp_path / "sale_order_view.xml"

    xml_file.write_text(
        """
<odoo>

    <record id="view_sale_order_custom" model="ir.ui.view">

        <field name="model">
            sale.order
        </field>

        <field name="arch" type="xml">

            <xpath expr="//field[@name='amount_total']"
                   position="after">

                <field name="x_custom_total"/>

            </xpath>

        </field>

    </record>

</odoo>
""",
        encoding="utf-8",
    )

    result = XMLAnalyzer().analyze(
        str(xml_file)
    )

    view = result["views"][0]

    assert len(view["xpaths"]) == 1

    xpath = view["xpaths"][0]

    assert xpath["expr"] == "//field[@name='amount_total']"
    assert xpath["position"] == "after"

def test_reports(tmp_path):
    xml_file = tmp_path / "report.xml"

    xml_file.write_text(
        """
<odoo>

    <record id="action_report_sale_order"
            model="ir.actions.report">

        <field name="name">
            Sale Order
        </field>

        <field name="model">
            sale.order
        </field>

        <field name="report_type">
            qweb-pdf
        </field>

        <field name="report_name">
            custom_sale_order.report_sale_order
        </field>

    </record>

</odoo>
""",
        encoding="utf-8",
    )

    result = XMLAnalyzer().analyze(
        str(xml_file)
    )

    assert len(result["reports"]) == 1

    report = result["reports"][0]

    assert report["id"] == "action_report_sale_order"
    assert report["model"] == "sale.order"
    assert report["report_type"] == "qweb-pdf"
    assert report["report_name"] == (
        "custom_sale_order.report_sale_order"
    )