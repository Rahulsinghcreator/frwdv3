from all_db import legend_db


def total_limit_id():
    return legend_db.get_key("LIMIT") or {}


def is_id_limit(chat_id):
    ok = total_limit_id()
    if chat_id in ok:
        return True
    return False


def add_limit(chat_id, count):
    ok = total_limit_id()
    ok.update({chat_id: count})
    return legend_db.set_key("LIMIT", ok)
