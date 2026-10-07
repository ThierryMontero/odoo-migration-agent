from agents.functional_analyzer import FunctionalAnalyzer


def test_functional_analysis():

    code_analysis = {
        "classes": ["SaleOrder"],
        "models": [],
        "inherits": ["sale.order"],
        "model_types": ["models.Model"],
        "descriptions": ["Custom Sale Order"],
        "fields": [
            "x_custom_total: Float",
        ],
        "api_decorators": ["depends"],
        "methods": ["_compute_custom_total"],
    }

    xml_analysis = {
        "views": [
            {
                "id": "view_sale_order_custom",
                "model": "sale.order",
                "type": "form",
                "fields": ["x_custom_total", "amount_total"],
                "xpaths": [
                    {
                        "expr": "//field[@name='amount_total']",
                        "position": "after",
                    }
                ],
            }
        ],
        "actions": ["action_sale_order_custom"],
        "menus": [
            {
                "id": "menu_sale_order_custom",
                "name": "Custom Sales",
            }
        ],
        "records": [
            {
                "id": "view_sale_order_custom",
                "model": "ir.ui.view",
            }
        ],
        "reports": [],
    }

    manifest = {
        "name": "Test Module",
        "version": "16.0.1.0.0",
        "depends": ["sale"],
        "data": ["views/sale_order_views.xml"],
    }

    analyzer = FunctionalAnalyzer()

    result = analyzer.analyze(
        code_analysis=code_analysis,
        xml_analysis=xml_analysis,
        manifest=manifest,
    )

    assert result["model"] == "sale.order"
    assert "x_custom_total" in result["custom_behavior"]
    assert "_compute_custom_total" in result["custom_behavior"]
    assert "view_sale_order_custom" in result["custom_behavior"]

    assert result["technical_elements"]["fields"] == [
        "x_custom_total: Float"
    ]

    assert result["technical_elements"]["methods"] == [
        "_compute_custom_total"
    ]

    assert len(result["technical_elements"]["xpaths"]) == 1

    assert result["technical_elements"]["xpaths"][0]["expr"] == (
        "//field[@name='amount_total']"
    )


def test_new_custom_model():

    code_analysis = {
        "classes": ["CustomModel"],
        "models": ["x.custom.model"],
        "inherits": [],
        "model_types": ["models.Model"],
        "descriptions": ["Custom Model"],
        "fields": [
            "name: Char",
        ],
        "api_decorators": [],
        "methods": [],
    }

    xml_analysis = {
        "views": [],
        "actions": [],
        "menus": [],
        "records": [],
        "reports": [],
    }

    analyzer = FunctionalAnalyzer()

    result = analyzer.analyze(
        code_analysis=code_analysis,
        xml_analysis=xml_analysis,
        manifest={},
    )

    assert result["model"] == "x.custom.model"
    assert "name" in result["custom_behavior"]
    assert result["technical_elements"]["fields"] == [
        "name: Char"
    ]


def test_xml_focused_module():

    code_analysis = {
        "classes": [],
        "models": [],
        "inherits": [],
        "model_types": [],
        "descriptions": [],
        "fields": [],
        "api_decorators": [],
        "methods": [],
    }

    xml_analysis = {
        "views": [
            {
                "id": "view_custom",
                "model": "sale.order",
                "type": "form",
                "fields": ["amount_total"],
                "xpaths": [
                    {
                        "expr": "//field[@name='amount_total']",
                        "position": "after",
                    }
                ],
            }
        ],
        "actions": ["action_custom"],
        "menus": [
            {
                "id": "menu_custom",
                "name": "Custom",
            }
        ],
        "records": [],
        "reports": [],
    }

    analyzer = FunctionalAnalyzer()

    result = analyzer.analyze(
        code_analysis=code_analysis,
        xml_analysis=xml_analysis,
        manifest={},
    )

    assert result["model"] == "sale.order"

    assert "view_custom" in result["custom_behavior"]

    assert result["technical_elements"]["actions"] == [
        "action_custom"
    ]

    assert result["technical_elements"]["menus"] == [
        {
            "id": "menu_custom",
            "name": "Custom",
        }
    ]

    assert len(result["technical_elements"]["xpaths"]) == 1