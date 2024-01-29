# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

_logger = logging.getLogger(__name__)


class WebsiteHrRecruitmentZeta(WebsiteHrRecruitment):
    def sitemap_jobs(self, rule, qs):
        if not qs or qs.lower() in "/jobs":
            yield {"loc": "/jobs"}

    @http.route(
        ["/jobs", "/jobs/label_ids/<models('hr.job.label'):label_filtered_ids>"],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_jobs,
    )
    def jobs(self, label_filtered_ids=None, **kwargs):
        res = super(WebsiteHrRecruitmentZeta, self).jobs(
            None, None, None, None, **kwargs
        )
        env = request.env(
            context=dict(request.env.context, show_address=True, no_tag_br=True)
        )

        context = res.qcontext
        jobs = context["jobs"]
        _logger.info(label_filtered_ids)
        _logger.info(kwargs)

        if label_filtered_ids:
            label_ids = env["hr.job.label"].browse(label_filtered_ids)
            for cat in label_ids.category_id:
                cat_label_ids = label_ids.filtered(lambda r: r.category_id == cat)
                remaining_jobs = []
                for job in jobs:
                    if set(cat_label_ids.ids) & set(job.label_ids.ids):
                        remaining_jobs.append(job)
                        # _logger.info(label_filtered_ids)
            #     _logger.info(set(label_filtered_ids).issubset(job.label_ids.ids))
            # jobs = jobs.filtered(
            #     lambda r: set(label_filtered_ids).issubset(r.label_ids.ids)
            # )
        label_split_up = []
        categories = env["hr.job.label.category"].search([])
        _logger.info(categories)
        all_jobs = env["hr.job"].search([])
        for cat in categories:
            _logger.info(cat.label_ids)
            if not cat.label_ids:
                continue
            cat_dict = {"category": cat}
            amount_of_labels_used = 0
            children = []
            for label in cat.label_ids.sorted(key=lambda r: r.sequence):
                _logger.info("_______")
                _logger.info(label)
                if all_jobs.filtered(lambda r: label in r.label_ids):
                    amount_of_labels_used += 1
                    children.append(
                        {
                            "label": label,
                            "count": len(jobs.filtered(lambda r: label in r.label_ids)),
                        }
                    )
                _logger.info(children)
            if amount_of_labels_used >= 2:
                cat_dict["children"] = children
                label_split_up.append(cat_dict)
            _logger.info(cat_dict)

        _logger.info(label_split_up)
        res.qcontext.update({"jobs": jobs, "labels_split_up": label_split_up})
        return res
