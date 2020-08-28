import json

def get_user_email_domain(user_email):
    user_email_domain = user_email.split('@')[1]
    return user_email_domain

def reverse_email_domain(user_email_domain):
    split_domain = user_email_domain.split('.')
    split_domain.reverse()
    reversed_user_email_domain = '.'.join(split_domain)
    return reversed_user_email_domain

def get_subentities(user_email_domain):
    reversed_user_email_domain = reverse_email_domain(user_email_domain)
    try:
        with open(f"./app/geojson/{reversed_user_email_domain}.geojson") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    subentities = data["features"][0]["properties"].get("subentities")
    return subentities