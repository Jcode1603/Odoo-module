# -*- coding: utf-8 -*-
###################################################################################
#    Odoo Mates
#    Copyright (C) 2021-TODAY Odoo Mates.
#
#    This program is free software: you can modify

#
###################################################################################
{
    'name': 'Farmer records',
    'version': '1.3',
    'summary': """Data inputs for farm products""",
    'description': """Data inputs for farm products""",
    'category': 'Project',
    'author': 'Joshua Opeyemi',
    'company': 'PSE',
    'maintainer': 'PSE',
    'website': 'http://infinera.com',
    'depends': ['base', 'project', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/farmers_accounts.xml',
    ],
    'demo': [
        'security/ir.model.access.csv',
        'views/farmers_accounts.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
