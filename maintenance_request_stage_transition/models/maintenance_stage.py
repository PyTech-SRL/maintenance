# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from lxml import etree

from odoo import _, fields, models
from odoo.osv.expression import OR


class MaintenanceStage(models.Model):

    _inherit = "maintenance.stage"

    next_stage_ids = fields.Many2many(
        "maintenance.stage",
        string="Next stages",
        relation="maintenance_stage_next_stage",
        column1="stage_id",
        column2="next_stage_id",
    )
    previous_stage_ids = fields.Many2many(
        "maintenance.stage",
        string="Previous stages",
        relation="maintenance_stage_next_stage",
        column1="next_stage_id",
        column2="stage_id",
    )
    button_class = fields.Selection(
        [
            ("primary", "Primary"),
            ("info", "Info"),
            ("success", "Success"),
            ("warning", "Warning"),
            ("danger", "Danger"),
        ],
        help="For default, the system uses primary",
    )

    team_ids = fields.Many2many("maintenance.team",)

    def _get_stage_node_attrs(self):
        domain = [("stage_id", "not in", self.previous_stage_ids.ids)]
        if self.team_ids:
            domain = OR(
                [domain, [("maintenance_team_id", "not in", self.team_ids.ids)]]
            )
        return {"invisible": domain}

    def _get_stage_node_name(self):
        return _("To %s") % self.name

    def _get_stage_node(self):
        return etree.Element(
            "button",
            attrib={
                "name": "set_maintenance_stage",
                "id": str(self.id),
                "type": "object",
                "class": "btn-%s" % (self.button_class or "primary"),
                "context": json.dumps({"next_stage_id": self.id}),
                "attrs": json.dumps(self._get_stage_node_attrs()),
                "string": self._get_stage_node_name(),
            },
        )
