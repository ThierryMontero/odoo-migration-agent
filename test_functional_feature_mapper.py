from agents.functional_feature_mapper import FunctionalFeatureMapper


def test_map_computed_field():

    functional_analysis = {
        "model": "sale.order",
        "technical_elements": {
            "fields": [
                "x_custom_total: Float",
            ],
            "field_metadata": [
                {
                    "name": "x_custom_total",
                    "type": "Float",
                    "compute": "_compute_custom_total",
                    "store": None,
                    "related": None,
                    "readonly": None,
                },
            ],
            "methods": [
                "_compute_custom_total",
            ],
            "views": [],
            "xpaths": [],
            "actions": [],
            "reports": [],
            "menus": [],
        },
    }

    mapper = FunctionalFeatureMapper()

    result = mapper.map(functional_analysis)

    assert len(result["features"]) == 1

    feature = result["features"][0]

    assert feature["type"] == "computed_field"
    assert feature["name"] == "x_custom_total"
    assert feature["model"] == "sale.order"


def test_map_view_inheritance():

    functional_analysis = {
        "model": "sale.order",
        "technical_elements": {
            "fields": [],
            "methods": [],
            "views": [
                {
                    "id": "view_sale_order_custom",
                    "model": "sale.order",
                    "type": "form",
                    "fields": [],
                    "xpaths": [
                        {
                            "expr": "//field[@name='amount_total']",
                            "position": "after",
                        }
                    ],
                }
            ],
            "xpaths": [],
            "actions": [],
            "reports": [],
            "menus": [],
        },
    }

    mapper = FunctionalFeatureMapper()

    result = mapper.map(functional_analysis)

    assert len(result["features"]) == 1

    feature = result["features"][0]

    assert feature["type"] == "view_inheritance"
    assert feature["name"] == "view_sale_order_custom"
    assert feature["model"] == "sale.order"


def test_map_window_action():

    functional_analysis = {
        "model": "sale.order",
        "technical_elements": {
            "fields": [],
            "methods": [],
            "views": [],
            "xpaths": [],
            "actions": [
                "action_sale_order_custom",
            ],
            "reports": [],
            "menus": [],
        },
    }

    mapper = FunctionalFeatureMapper()

    result = mapper.map(functional_analysis)

    assert len(result["features"]) == 1

    feature = result["features"][0]

    assert feature["type"] == "window_action"
    assert feature["name"] == "action_sale_order_custom"
    assert feature["model"] == "sale.order"


def test_simple_field_is_not_computed_field():

    functional_analysis = {
        "model": "sale.order",
        "technical_elements": {
            "fields": [
                "x_custom_reference: Char",
            ],
            "methods": [],
            "views": [],
            "xpaths": [],
            "actions": [],
            "reports": [],
            "menus": [],
        },
    }

    mapper = FunctionalFeatureMapper()

    result = mapper.map(functional_analysis)

    assert result["features"] == []

def test_map_computed_field_from_metadata():

    functional_analysis = {
        "model": "sale.order",
        "technical_elements": {
            "fields": [
                "x_custom_total: Float",
                "x_custom_reference: Char",
            ],
            "field_metadata": [
                {
                    "name": "x_custom_total",
                    "type": "Float",
                    "compute": "_compute_custom_total",
                    "store": True,
                    "related": None,
                    "readonly": None,
                },
                {
                    "name": "x_custom_reference",
                    "type": "Char",
                    "compute": None,
                    "store": None,
                    "related": None,
                    "readonly": True,
                },
            ],
            "methods": [
                "_compute_custom_total",
            ],
            "views": [],
            "xpaths": [],
            "actions": [],
            "reports": [],
            "menus": [],
        },
    }

    mapper = FunctionalFeatureMapper()

    result = mapper.map(functional_analysis)

    assert len(result["features"]) == 1

    feature = result["features"][0]

    assert feature["type"] == "computed_field"
    assert feature["name"] == "x_custom_total"
    assert feature["model"] == "sale.order"

    assert feature["evidence"]["compute_method"] == (
        "_compute_custom_total"
    )
