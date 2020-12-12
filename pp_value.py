# calculate pp value for a dict nag -> [pp pool, place chance]
# return a dictionary nag -> value

pool_size = 0

def set_pool_size(dict):
    global pool_size
    pool_size += [x[0] for x in dict.values()]

def calc_pp_value(dict):
    set_pool_size(dict)
    field_size = len(dict)
    if field_size <= 4:
        return calc_pp_value_1(dict)
    elif field_size <= 7:
        return calc_pp_value_2(dict)
    elif field_size <= 16:
        return calc_pp_value_3(dict)
    else:
        return calc_pp_value_4(dict)

def calc_pp_value_1(dict):
    result = {}
    for nag in dict:
        pp_pool_perc = dict(nag)[0]/pool_size
        place_chance = dict(nag)[1]
        pp_pool_value = (1 / pp_pool_perc) * place_chance
        result[nag] = pp_pool_value
    return result

def calc_pp_value_2(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict(nag_1)[0]/pool_size
        place_chance_1 = dict(nag_1)[1]
        result[nag_1] = 0
        for nag_2 in dict:
            if nag_2 is not nag_1:
                pp_pool_perc_2 = dict(nag_2)[0] / pool_size
                place_chance_2 = dict(nag_2)[1]
                pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2)) * \
                                (place_chance_1 * place_chance_2)
                result[nag_1] += pp_pool_value
    return result

def calc_pp_value_3(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict(nag_1)[0]/pool_size
        place_chance_1 = dict(nag_1)[1]
        result[nag_1] = 0
        for nag_2 in dict:
            if nag_2 is not nag_1:
                pp_pool_perc_2 = dict(nag_2)[0] / pool_size
                place_chance_2 = dict(nag_2)[1]
                for nag_3 in dict:
                    if nag_3 not in [nag_1, nag_2]:
                        pp_pool_perc_3 = dict(nag_3)[0] / pool_size
                        place_chance_3 = dict(nag_3)[1]
                        pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2 + pp_pool_perc_3)) * \
                                        (place_chance_1 * place_chance_2 * place_chance_3)
                        result[nag_1] += pp_pool_value
    return result

def calc_pp_value_4(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict(nag_1)[0]/pool_size
        place_chance_1 = dict(nag_1)[1]
        result[nag_1] = 0
        for nag_2 in dict:
            if nag_2 is not nag_1:
                pp_pool_perc_2 = dict(nag_2)[0] / pool_size
                place_chance_2 = dict(nag_2)[1]
                for nag_3 in dict:
                    if nag_3 not in [nag_1, nag_2]:
                        pp_pool_perc_3 = dict(nag_3)[0] / pool_size
                        place_chance_3 = dict(nag_3)[1]
                        for nag_4 in dict:
                            if nag_4 not in [nag_1, nag_2, nag_3]:
                                pp_pool_perc_4 = dict(nag_4)[0] / pool_size
                                place_chance_4 = dict(nag_4)[1]
                                pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2 + pp_pool_perc_3 + pp_pool_perc_4)) * \
                                                (place_chance_1 * place_chance_2 * place_chance_3 + place_chance_4)
                                result[nag_1] += pp_pool_value
    return result
