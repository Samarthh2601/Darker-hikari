def format_channels(data) -> dict:
    welcome = data.welcome
    leave = data.leave
    log = data.log
    vent = data.vent
    ret_dict = {}
    if welcome == 0:
        ret_dict.update({"welcome": "No welcome channel has been configurd yet!"})
    else:
        ret_dict.update({"welcome": f"<#{welcome}>"})

    if leave == 0:
        ret_dict.update({"leave": "No leave channel has been configurd yet!"})
    else:
        ret_dict.update({"leave": f"<#{leave}>"})

    if log == 0:
        ret_dict.update({"log": "No log channel has been configurd yet!"})
    else:
        ret_dict.update({"log": f"<#{log}>"})

    if vent == 0:
        ret_dict.update({"vent": "No vent channel has been configurd yet!"})
    else:
        ret_dict.update({"vent": f"<#{vent}>"})
    return ret_dict