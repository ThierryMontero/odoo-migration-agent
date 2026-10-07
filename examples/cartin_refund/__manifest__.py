{
    "name": "Cartin Refund",
    "version": "16.0.1.0.0",
    "summary": "Gestion des remboursements Cartin",

    "depends": [
        "base",
        "account",
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/refund_views.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "cartin_refund/static/src/js/refund.js",
        ],
    },

    "installable": True,
    "application": False,
}
