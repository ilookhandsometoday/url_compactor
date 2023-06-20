def remove_schema(url: str):
    return url.replace('https://', '').replace('http://', '')


def path_from_short_url(short_url: str):
    return short_url.split('/')[-1]
