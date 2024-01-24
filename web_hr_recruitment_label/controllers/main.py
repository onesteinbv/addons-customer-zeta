# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools
import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

_logger = logging.getLogger(__name__)


def job_routes():
    prefix = "/jobs"
    filters = [
        '/country/<model("res.country"):country>',
        '/department/<model("hr.department"):department>',
        "/office/<int:office_id>",
        "/employment_type/<int:contract_type_id>",
        "/label/<int:label_id>",
        # "/label/<models('hr.job.label'):label_filtered_ids>",
    ]
    routes = ["/jobs"]
    for L in range(len(filters) + 1):
        for subset in itertools.combinations(filters, L):
            routes.append(prefix + "".join(subset))
    return routes


class WebsiteHrRecruitmentLabel(WebsiteHrRecruitment):
    def sitemap_jobs(self, rule, qs):
        if not qs or qs.lower() in "/jobs":
            yield {"loc": "/jobs"}

    @http.route(
        job_routes(), type="http", auth="public", website=True, sitemap=sitemap_jobs
    )
    def jobs(
        self,
        country=None,
        department=None,
        office_id=None,
        contract_type_id=None,
        label_id=None,
        **kwargs
    ):
        res = super(WebsiteHrRecruitmentLabel, self).jobs(
            country, department, office_id, contract_type_id, **kwargs
        )
        env = request.env(
            context=dict(request.env.context, show_address=True, no_tag_br=True)
        )

        context = res.qcontext
        labels = env["hr.job"].search([("label_ids", "!=", False)]).label_ids
        jobs = context["jobs"]
        if label_id:
            jobs = [j for j in jobs if j.label_ids and label_id in j.label_ids.ids]

        res.qcontext.update({"jobs": jobs, "labels": labels, "label_id": label_id})
        return res
