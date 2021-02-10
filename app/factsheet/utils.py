from app.models import Sheet


def url_sheet(id):
    sheet = Sheet.query.get_or_404(id)
    policy = sheet.policy.lower().replace(' ', '_')
    target = sheet.target.lower().replace(' ', '_')

    return policy + '-' + target


def policy_target_from_url(url):
    policy, target = url.split('-')
    policy = policy.replace('_', ' ').lower()
    target = target.replace('_', ' ').lower()
    return policy, target
