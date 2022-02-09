# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PartnerLoan(models.Model):
    _name = "partner.loan"
    _description = "Loans for partners"

    name = fields.Char(string="Name", compute="_compute_name")
    partner_id = fields.Many2one("res.partner", string="Applicant", required=True)
    date = fields.Date(string="Date", default=datetime.today())
    fees = fields.Integer(string="Term", default=1, required=True)
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    amount_total = fields.Monetary(string="Amount Total", required=True)
    disabled = fields.Boolean(string="Disabled", default=True, compute="_compute_disabled")
    line_ids = fields.One2many("partner.loan.line", "loan_id", string="Loan Lines")

    @api.depends("partner_id", "date")
    @api.onchange("partner_id", "date")
    def _compute_name(self):
        for record in self:
            record.name = "Loan for %s on date %s" % (record.partner_id.name, record.date.strftime("%d-%m-%Y"))
    
    @api.constrains("fees")
    def _constraints_loan(self):
        for record in self:
            if record.fees < 1:
                raise ValidationError("Terms must be an integer >= 1.")

    @api.onchange("amount_total", "fees", "date")
    def generate_payment_lines(self):
        for record in self:
            if record.fees and record.amount_total and record.partner_id:
                # copy record before unlink
                fees = record.fees
                amount_total = record.amount_total
                date = record.date
                id = record._origin.id

                for line in record.line_ids:
                    line.unlink()

                # restore original record 
                record.fees = fees
                record.amount_total = amount_total
                record.date = date
                record._origin_id = id

                for i in range(1, record.fees + 1):
                    self.env["partner.loan.line"].create({
                        "payment_date": record.date + relativedelta(months=+i),
                        "amount": record.amount_total / record.fees,
                        "loan_id": record._origin_id
                    })

    
    @api.onchange("partner_id", "date", "amount_total", "fees")
    def _compute_disabled(self):
        for record in self:
            if record.fees and record.amount_total and record.partner_id:
                record.disabled = False


class PartnerLoan(models.Model):
    _name = "partner.loan.line"
    _description = "Line for partners loans"

    payment_date = fields.Date(string="Payment Date", required=True)
    amount = fields.Float(string="Amount")
    loan_id = fields.Many2one("partner.loan", string="Loan", required=True)
    currency_id = fields.Many2one("res.currency", string="Currency", related="loan_id.currency_id")

