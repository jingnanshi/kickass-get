import requests
import data

def choose_mirror(url_list):
    """ choose working mirror out of a list
    """
    for url in url_list:
        print 'Checking connection at {}.'.format(url)
        status_code = check_connection(url)
        if status_code != 0 and status_code != 404:
            print 'Connection at {} succeeded.'.format(url)
            return url
        else:
            'Connection failed, code {}.'.format(str(status_code))
    return None

def check_connection(url):
    """ check connection to the provided url, 
        return status code
    """
    try:
        resp = requests.head(url, timeout=data.default_timeout)
        return resp.status_code
    except requests.exceptions.ConnectionError:
        return 0
    except requests.exceptions.Timeout:
        return 0