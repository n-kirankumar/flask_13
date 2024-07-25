from log import log_message
from constants import LOG_MESSAGES
from data import data
from constants import VALID_COUNTRY_LIST, EXCLUDED_NUMBERS, VALID_GENDERS, VALID_BLOOD_GROUPS


def validate_user_data(user_data):
    # Placeholder function for validating user data
    return True


def get_user_info(username, current_user, is_admin):
    if username not in data["records"]:
        log_message('error', LOG_MESSAGES['user_not_found'])
        raise ValueError(LOG_MESSAGES['user_not_found'])

    user_info = data["records"][username]
    if not is_admin and current_user != username:
        log_message('error', LOG_MESSAGES['unauthorized_access'])
        raise PermissionError(LOG_MESSAGES['unauthorized_access'])

    log_message('info', LOG_MESSAGES['user_info'])
    return user_info


def list_all_users(current_user, is_admin):
    if not is_admin:
        log_message('error', LOG_MESSAGES['unauthorized_list_users'])
        raise PermissionError(LOG_MESSAGES['unauthorized_list_users'])

    log_message('info', LOG_MESSAGES['list_all_users'])
    return data["records"]


def create_user_profile(username, user_data):
    if username in data["records"]:
        log_message('error', LOG_MESSAGES['user_exists'])
        raise ValueError(LOG_MESSAGES['user_exists'])

    if validate_user_data(user_data):
        data["records"][username] = user_data
        log_message('info', LOG_MESSAGES['user_created'])
        return user_data
    raise ValueError(LOG_MESSAGES['invalid_email'])


def update_user_info(username, user_data, current_user, is_admin):
    if username not in data["records"]:
        log_message('error', LOG_MESSAGES['user_not_found'])
        raise ValueError(LOG_MESSAGES['user_not_found'])

    if not is_admin and current_user != username:
        log_message('error', LOG_MESSAGES['unauthorized_update'])
        raise PermissionError(LOG_MESSAGES['unauthorized_update'])

    if validate_user_data(user_data):
        data["records"][username].update(user_data)
        log_message('info', LOG_MESSAGES['user_updated'])
        return data["records"][username]
    raise ValueError(LOG_MESSAGES['invalid_email'])
