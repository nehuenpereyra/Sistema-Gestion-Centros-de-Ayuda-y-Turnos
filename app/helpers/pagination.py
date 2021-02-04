from flask import request, url_for


def url_for_page(url, page, **kwargs):
    """Returns a url with all the current parameters of the url more the current page of the page.

    Keyword arguments:
    url -- string url to address
    page -- integer actual page
    kwargs -- dictionary arguments
    """
    args = {**request.args.copy(), **kwargs}
    args["page"] = page

    return url_for(url, **args)
