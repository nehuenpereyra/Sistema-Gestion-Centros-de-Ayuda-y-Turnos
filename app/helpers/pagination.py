
from flask import request, url_for


def url_for_page(url, page):
    args = request.args.copy()
    args["page"] = page
    return url_for(url, **args)
