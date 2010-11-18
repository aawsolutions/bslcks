from apikeys.models import Key

def allkeys(target_domain):
    try:
        keys = Key.objects.filter(site__domain=target_domain)
    except:
        keys = "ERROR"
    return keys
