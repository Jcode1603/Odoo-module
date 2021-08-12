from odoo import api, fields, models  # imports fields module and models module


class Farm_Customers(models.Model):
    _name = 'farmers.infinera'  # this will appear in the data base as model_name
    _description = 'Financial Expenditure records for farmers with Infinera'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.onchange('name')
    def set_form_values(self):
        for rec in self:
            if rec.name:
                rec.cluster_id = rec.name.x_studio_cluster_id_1
                rec.email = rec.name.x_studio_last_name
                rec.phone = rec.name.phone
                rec.lga = rec.name.x_studio_lga_name
                rec.comm_association = rec.name.x_studio_commodity_association
                rec.state = rec.state_id
                rec.crop_type = rec.x_studio_produce_funded

    @api.depends('input_costs.final_cost')
    def _compute_input_totals(self):
        for record in self:
            record.input_total = sum(line.final_cost for line in record.input_costs)

    @api.depends('mech_costs.Totalcost')
    def _compute_mech_totals(self):
        for record in self:
            record.mech_total = sum(line.Totalcost for line in record.mech_costs)

    @api.depends('labour_costs.Totalcost')
    def _compute_labour_totals(self):
        for record in self:
            record.labour_total = sum(line.Totalcost for line in record.labour_costs)

    @api.depends('input_total', 'mech_total', 'labour_total')
    def _compute_sub_total(self):
        for rec in self:
            rec.sub_total = rec.input_total+rec.mech_total+rec.labour_total

    @api.depends('sub_total', 'insuranceval')
    def _compute_insurance_total(self):
        for record in self:
            record.insurance_amount = (record.insuranceval / 100) * record.sub_total

    @api.depends('sub_total', 'mande_val')
    def _compute_mande(self):
        for record in self:
            record.mande_amount = (record.mande_val / 100) * record.sub_total

    @api.depends('sub_total', 'adminfee_val')
    def _compute_adminfee(self):
        for record in self:
            record.admin_amount = (record.adminfee_val / 100) * record.sub_total

    @api.depends('sub_total', 'insurance_amount', 'mande_amount', 'admin_amount', 'LoanRecovery', 'Extension')
    def _compute_total_prod(self):
        for record in self:
            record.total_production = record.sub_total+record.insurance_amount+record.mande_amount+record.admin_amount+record.LoanRecovery+record.Extension

    '''@api.depends('input_costs.final_cost', 'mech_costs.Totalcost', 'labour_costs.Totalcost')
    def _compute_sub_total(self):
        for rec in self:
            rec.sub_total = sum([line.finalcost, rec2.Totalcost, record.Totalcost] for line in rec.input_costs for rec2 in rec.mech_costs for record in rec.labour_costs)'''

    #farm details field
    name = fields.Many2one('res.partner', string="Farmer's Name", required=True)  # this creates a variable 'name' with a character type field
    user_id = fields.Many2one('res.users')
    email = fields.Char(string='Last Name', required=True)
    phone = fields.Char(string='Farmer Telephone')
    address = fields.Char(string='Address')
    crop_type = fields.Selection(string='Produce Funded',[('maize', 'Maize'), ('soybeans', 'Soybeans'), ('sorghum', 'Sorghum'), ('cowpea', 'Cowpea'), ('sesame', 'Sesame'), ('rice', 'Rice'), ('cassava', 'Cassava')], string='Crop type')
    cluster_id = fields.Char(string='Cluster ID')
    comm_association = fields.Char(string='Commodity Association')
    farm_size = fields.Integer(string='Farm Size', default=1)
    state = fields.Char(string='State')
    city = fields.Char(string='City')
    lga = fields.Char(string='LGA name')
    zip = fields.Char(string='Zip code')
    #services fields
    currency_id = fields.Many2one('res.currency', string='Currency')
    LoanRecovery = fields.Monetary(string='Loan Recovery')
    Extension = fields.Monetary(string='Extension')
    insuranceval = fields.Float(string='insurance%', default=3.5)
    mande_val = fields.Float(string='M&E%', default=2.5)
    adminfee_val = fields.Float(string='Admin fee%', default=2.5)
    color = fields.Integer()
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    # activity_ids = fields.One2many('mail.activity', 'calendar_event_id', string='Activities')
    kanban_state = fields.Selection([('normal', 'In Progress'), ('done', 'Done'), ('blocked', 'Blocked')],
                                    default='normal')
    program = fields.Many2one('farm.program')
    form_state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string='Status')
    input_costs = fields.Many2many('farm.eop.inputcost')
    mech_costs = fields.Many2many('farm.mech')
    labour_costs = fields.Many2many('labour.farm')
    sub_total = fields.Monetary(compute='_compute_sub_total', store=True, string='Sub total')
    input_total = fields.Float(compute='_compute_input_totals')
    mech_total = fields.Float(compute='_compute_mech_totals')
    labour_total = fields.Float(compute='_compute_labour_totals')
    insurance_amount = fields.Monetary(compute='_compute_insurance_total', store=True, string='Insurance Amount')
    mande_amount = fields.Monetary(compute='_compute_mande', store=True, string='M&E Amount')
    admin_amount = fields.Monetary(compute='_compute_adminfee', store=True, string='Admin Fee')
    total_production = fields.Monetary(compute='_compute_total_prod', store=True, string='Total production costs')


class Farm_Programs(models.Model):
    _name = 'farm.program'
    _description = 'This class creates different farmer programs'
    _rec_name = 'prog_name'

    prog_name = fields.Char(string='Name')
    prog_desc = fields.Char(string='Description')
    color = fields.Integer()
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    program_state = fields.Selection([('normal', 'In Progress'), ('done', 'Done'), ('blocked', 'Blocked')],
                                    default='normal')

    '''@api.depends('prog_name')
    def action_view_accounts(self):
        action = self.with_context(active_id=self.id, active_ids=self.ids) \
            .env.ref('Farmers_account.action_account_link') \
            .sudo().read()[0]
        action['display_name'] = self.name
        return action'''


class Input_cost(models.Model):
    _name = 'farm.eop.inputcost'
    _description = 'this class computes the input cost of different farm products'

    @api.depends('size', 'quantity_required')
    def to_give(self):
        for give in self:
            give.quantity_given = give.size*give.quantity_required

    @api.depends('unit_cost')
    def final(self):
        for tot in self:
            tot.final_cost = tot.unit_cost*tot.quantity_required*tot.size

    description = fields.Char(string='Description')
    size = fields.Integer(string='Size')
    quantity_required = fields.Integer(string='Quantity')
    units = fields.Char(string='Unit')
    quantity_given = fields.Integer(string='Quantity to be given', compute='to_give')
    currency_id = fields.Many2one('res.currency', string='currency')
    unit_cost = fields.Monetary(string='Unit Cost')
    final_cost = fields.Monetary(string='Total cost per Ha', compute='final')


class Farm_mechanization(models.Model):
    _name = 'farm.mech'
    _description = 'for computing the mechanization costs on the farm'

    @api.depends('cost_per_unit', 'quantity')
    def mech_cost(self):
        for mech in self:
            mech.Totalcost = mech.cost_per_unit*mech.quantity

    description = fields.Char(string='description')
    currency_id = fields.Many2one('res.currency', string='currency')
    cost_per_unit = fields.Monetary(string='cost per unit')
    quantity = fields.Integer(string='quantity required')
    Totalcost = fields.Monetary(string='Total cost per Ha', compute='mech_cost', store=True)


class Labour_cost(models.Model):
    _name = 'labour.farm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'for computing the labour costs on the farm'

    @api.depends('costperunit', 'quantity')
    def work_cost(self):
        for work in self:
            work.Totalcost = work.costperunit*work.quantity

    labour_task = fields.Char(string='description')
    worker = fields.Char(string='Labour Type')
    quantity = fields.Integer(string='No of Labourers')
    currency_id = fields.Many2one('res.currency', string='currency')
    costperunit = fields.Monetary(string='cost per labourer')
    Totalcost = fields.Monetary(string='Total cost labourer', compute='work_cost', store=True)
    totally = fields.Many2one('totals.total', 'Total value')
    #totalfields = fields.Integer(string='Total', compute='_total_field', store=True, compute_sudo=True, readonly=False, currency_field='currency_id')


class Totals(models.Model):
    _name = 'totals.total'
    _description = 'Total of operations modules'

    @api.depends('total_fields.Totalcost')
    def _compute_totals(self):
        for record in self:
            record.total = sum(line.Totalcost for line in record.total_fields)

    total_fields = fields.One2many('labour.farm', 'totally')
    name = fields.Many2one('labour.farm')
    total = fields.Float(compute='_compute_totals', store=True)


'''
this models is no longer in use
class Services(models.Model):
    _name = 'farm.services.inf'

    serv_name = fields.Char(string='Service Name')
    LoanRecovery = fields.Char(string='Loan Recovery')
    Extension = fields.Char(string='Extension')
    insuranceval = fields.Float(string='insurance%')
    mande_val = fields.Float(string='M&E%')
    adminfee_val = fields.Float(string='Admin fee') '''
