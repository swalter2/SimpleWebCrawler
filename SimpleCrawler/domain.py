from urllib.parse import urlparse


# Get domain name
def get_domain_name(page_url):
    try:
        results = get_sub_domain_name(page_url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get subdomain name
def get_sub_domain_name(page_url):
    try:
        return urlparse(page_url).netloc
    except:
        return ''


