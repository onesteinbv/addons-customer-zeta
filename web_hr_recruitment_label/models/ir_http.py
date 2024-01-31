import logging

from odoo import models

from odoo.addons.base.models import ir_http

_logger = logging.getLogger(__name__)


class ModelsConverter(ir_http.ModelsConverter):
    def to_python(self, value):
        return [int(x) for x in value.split(",")]

    def to_url(self, value):
        return ",".join([str(i) for i in value])


class IrHttp(models.AbstractModel):
    _inherit = ["ir.http"]

    rerouting_limit = 10

    @classmethod
    def _get_converters(cls):
        """Get the converters list for custom url pattern werkzeug need to
        match Rule. This override adds the website ones.
        """
        return dict(
            super(IrHttp, cls)._get_converters(),
            models=ModelsConverter,
        )
