from agents.odoo19_documentation_resolver import (
    Odoo19DocumentationResolver,
)


def test_resolve_computed_field():

    resolver = Odoo19DocumentationResolver()

    result = resolver.resolve("computed_field")

    assert result["status"] == "NATIVE_FOUND"

    assert result["documentation"]["version"] == "19.0"

    assert result["documentation"]["category"] == "ORM"

    assert "url" in result["documentation"]

    assert result["confidence"] >= 0.9


def test_resolve_view_inheritance():

    resolver = Odoo19DocumentationResolver()

    result = resolver.resolve("view_inheritance")

    assert result["status"] == "NATIVE_FOUND"

    assert result["documentation"]["category"] == "Views"

    assert result["documentation"]["version"] == "19.0"

    assert "inheritance" in result["documentation"]["title"].lower()


def test_resolve_window_action():

    resolver = Odoo19DocumentationResolver()

    result = resolver.resolve("window_action")

    assert result["status"] == "NATIVE_FOUND"

    assert result["documentation"]["category"] == "Actions"

    assert result["documentation"]["version"] == "19.0"


def test_resolve_unknown_feature():

    resolver = Odoo19DocumentationResolver()

    result = resolver.resolve(
        "extremely_specific_custom_business_feature_xyz"
    )

    assert result["status"] == "UNCERTAIN"

    assert result["documentation"] is None
