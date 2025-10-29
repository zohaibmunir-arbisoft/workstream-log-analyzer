from datetime import datetime

# Rule-based checks
def check_hours_per_task(hours):
    return hours <= 3

def check_rule_2(log_date):
    today = datetime.today()
    log_dt = datetime.strptime(log_date, "%Y-%m-%d")
    return (today - log_dt).days <= 7

def check_description_len(log_description):
    """it will check number of words in each description
    and then return fail if it's less than 5 words"""

    description_words = log_description.split(' ')
    if len(description_words) > 5:
        return True
    else:
        return False