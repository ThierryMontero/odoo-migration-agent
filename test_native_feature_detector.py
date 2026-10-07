from agents.native_feature_detector import NativeFeatureDetector


def test_detect_custom_fields_and_methods():

    functional_analysis = {
        "type": "functional_analysis",
        "model": "sale.order",
        "custom_behavior": [
            "x_custom_total",
            "_compute_custom_total",
            "view_sale_order_custom",
        ],
        "technical_elements": {
            "fields": [
                "x_custom_total: Float",
            ],
            "methods": [
                "_compute_custom_total",
            ],
            "views": [
                {
                    "id": "view_sale_order_custom",
                    "model": "sale.order",
                    "type": "form",
                    "fields": ["x_custom_total"],
                    "xpaths": [],
                }
            ],
            "xpaths": [],
            "actions": [],
            "reports": [],
            "menus": [],
        },
    }

    detector = NativeFeatureDetector()

    result = detector.detect(functional_analysis)

    assert result["model"] == "sale.order"

    assert len(result["features"]) == 3

    feature_names = [
        feature["name"]
        for feature in result["features"]
    ]

    assert "x_custom_total" in feature_names
    assert "_compute_custom_total" in feature_names
    assert "view_sale_order_custom" in feature_names


def test_detect_actions_reports_and_menus():

    functional_analysis = {
        "type": "functional_analysis",
        "model": "sale.order",
        "custom_behavior": [],
        "technical_elements": {
            "fields": [],
            "methods": [],
            "views": [],
            "xpaths": [],
            "actions": [
                "action_sale_order_custom",
            ],
            "reports": [
                {
                    "id": "report_sale_order_custom",
                    "model": "sale.order",
                    "report_type": "qweb-pdf",
                    "report_name": "custom.sale_order",
                }
            ],
            "menus": [
                {
                    "id": "menu_sale_order_custom",
                    "name": "Custom Sales",
                }
            ],
        },
    }

    detector = NativeFeatureDetector()

    result = detector.detect(functional_analysis)

    assert len(result["features"]) == 3

    assert result["features"][0]["type"] == "action"
    assert result["features"][0]["name"] == "action_sale_order_custom"

    assert result["features"][1]["type"] == "report"
    assert result["features"][1]["name"] == "report_sale_order_custom"

    assert result["features"][2]["type"] == "menu"
    assert result["features"][2]["name"] == "menu_sale_order_custom"
