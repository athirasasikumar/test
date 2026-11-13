{
    'name': "Material Request",
    'version': '15.0.1.0.0',
    'author': "Athira",
    'category': 'Request',
    'application': True,
    'sequence': -1000,
    'depends': ['base','stock'],
    'data': [
        'security/material_request_group.xml',
        'security/ir.model.access.csv',
        'views/material_request.xml',
        'views/menu.xml',

    ]
}
