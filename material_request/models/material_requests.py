from odoo import fields, models, api


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Request ID", required=True,
                                 readonly=True, default='New')
    user_id = fields.Many2one('res.users', 'Current User',
                                  default=lambda self: self.env.user)
    product_id = fields.Many2one('product.product')
    requisition_date = fields.Date(string="Requisition Date")
    qty = fields.Float(string="Quantity")
    prod_ids = fields.One2many('product.list', 'product_list_ids')
    receives_from = fields.Selection([
        ('po', 'Purchase order'),
        ('internal', 'Internal Transfer'),])
    state= fields.Selection([
        ('submit', 'To Submit'),
        ('submitted', 'Submitted'),
        ('approved', 'ManagerApproved'),
        ('approve', 'HeadApproved'),
        ('rejected', 'Rejeted'),
        ('cancel', 'Cancel')],
        default='submit')

    def btn_submit(self):
            self.state = 'submitted'

    def btn_approved(self):
        self.state = 'approved'

    def btn_head_approve(self):
        self.state = 'approve'
        for line in self.prod_ids:
            if line.receives_from == 'po':
                for k in line.product_id:
                    c = k.sorted(lambda s: s.price)
                    print(k.name,c.price)
                    vals = []
                    vals.append((0, 0,
                          {
                              'product_id': line.product_id.id,
                              'product_qty': line.qty,
                          }))

                    rfq = self.env['purchase.order'].create({
                        'partner_id': c.seller_ids.name[0].id,
                        'order_line': vals,
                    })
                    print(c.seller_ids.name[0].id)

    def btn_refuse(self):
        self.state = 'rejected'

    def btn_cancel(self):
       self.state = 'cancel'

    def btn_draft(self):
        self.state = 'submit'

    # .....sequence number....

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'material.request') or 'New'
        res = super(MaterialRequest, self).create(vals)
        return res

    class ProductList(models.Model):
        _name = "product.list"

        product_list_ids = fields.Many2one('material.request')
        product_id = fields.Many2one('product.product', required=True)
        qty = fields.Float(string="Quantity", required=True)
        receives_from = fields.Selection([
            ('po', 'Purchase order'),
            ('internal', 'Internal Transfer'),
        ])

    #
    # vals = []
    #         vals.clear()
    #         for line in self.prod_id:
    #             if line.receives_from =='po':
    #                 vals.append((0, 0,
    #                              {
    #                                  'product_id': line.product_id.id,
    #                                  'product_qty': line.qty,
    #                              }))
    #     for partner in lines.product_id.seller_ids.name:
    #             rfq = self.env['purchase.order'].create({
    #                 'name': self.request_number,
    #                 'date_planned': self.requisition_date,
    #                 'partner_id': line.product_id.variant_seller_ids.name,
    #                 'product_id': self.prod_id,
    #                 'order_line': vals,
    #             })
    #         return {
    #             'res_id': rfq.id,
    #         }
    #
    #
