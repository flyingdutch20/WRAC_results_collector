# calculate pp value for a dict nag -> [pp pool, place chance]
# return a dictionary nag -> value

def set_pool_size(dict):
    global pool_size
    pool_size = 0
    for x in dict.values():
        pool_size += x[0]
    return pool_size

def calc_pp_value(dict):
    my_pool_size = set_pool_size(dict)
    if my_pool_size == 0:
        return {}
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
        pp_pool_perc = dict[nag][0]/pool_size
        win_chance = dict[nag][1]
        place_chance = dict[nag][2]
        pp_pool_value = (1 / pp_pool_perc) * win_chance
        result[nag] = [pp_pool_perc, pp_pool_value]
    return result

def calc_pp_value_2(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict[nag_1][0]/pool_size
        win_chance_1 = dict[nag_1][1]
        place_chance_1 = dict[nag_1][2]
        pp_pool_value_1 = 0
        nags = [nag_1]
        for nag_2 in dict:
            if nag_2 not in nags:
                pp_pool_perc_2 = dict[nag_2][0] / pool_size
                win_chance_2 = dict[nag_2][1]
                place_chance_2 = dict[nag_2][2]
                chance_1_2 = win_chance_1 * (win_chance_2 / (1 - win_chance_1))
                chance_2_1 = win_chance_2 * (win_chance_1 / (1 - win_chance_2))
                try:
                    pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2)) * \
                                    (chance_1_2 + chance_2_1)
                except:
                    pp_pool_value = 0
                pp_pool_value_1 += pp_pool_value
        result[nag_1] = [pp_pool_perc_1, pp_pool_value_1]
    return result

def calc_pp_value_3(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict[nag_1][0]/pool_size
        win_chance_1 = dict[nag_1][1]
        place_chance_1 = dict[nag_1][2]
        pp_pool_value_1 = 0
        nags = [nag_1]
        for nag_2 in dict:
            if nag_2 not in nags:
                nags.append(nag_2)
                pp_pool_perc_2 = dict[nag_2][0] / pool_size
                win_chance_2 = dict[nag_2][1]
                place_chance_2 = dict[nag_2][2]
                for nag_3 in dict:
                    if nag_3 not in nags:
                        pp_pool_perc_3 = dict[nag_3][0] / pool_size
                        win_chance_3 = dict[nag_3][1]
                        place_chance_3 = dict[nag_3][2]
                        chance_1_2_3 = win_chance_1 * (win_chance_2 / (1 - win_chance_1)) * (win_chance_3 / (1 - win_chance_1 - win_chance_2))
                        chance_1_3_2 = win_chance_1 * (win_chance_3 / (1 - win_chance_1)) * (win_chance_2 / (1 - win_chance_1 - win_chance_3))
                        chance_2_1_3 = win_chance_2 * (win_chance_1 / (1 - win_chance_2)) * (win_chance_3 / (1 - win_chance_2 - win_chance_1))
                        chance_2_3_1 = win_chance_2 * (win_chance_3 / (1 - win_chance_2)) * (win_chance_1 / (1 - win_chance_2 - win_chance_3))
                        chance_3_1_2 = win_chance_3 * (win_chance_1 / (1 - win_chance_3)) * (win_chance_2 / (1 - win_chance_3 - win_chance_1))
                        chance_3_2_1 = win_chance_3 * (win_chance_2 / (1 - win_chance_3)) * (win_chance_1 / (1 - win_chance_3 - win_chance_2))
                        try:
                            pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2 + pp_pool_perc_3)) * \
                                            (chance_1_2_3 + chance_1_3_2 + chance_2_1_3 + chance_2_3_1 + chance_3_1_2 + chance_3_2_1)
                        except:
                            pp_pool_value = 0
                        pp_pool_value_1 += pp_pool_value
        result[nag_1] = [pp_pool_perc_1, pp_pool_value_1]
    return result

def calc_pp_value_4(dict):
    result = {}
    for nag_1 in dict:
        pp_pool_perc_1 = dict[nag_1][0]/pool_size
        win_chance_1 = dict[nag_1][1]
        place_chance_1 = dict[nag_1][2]
        pp_pool_value_1 = 0
        nags = [nag_1]
        for nag_2 in dict:
            if nag_2 not in nags:
                nags.append(nag_2)
                pp_pool_perc_2 = dict[nag_2][0] / pool_size
                win_chance_2 = dict[nag_2][1]
                place_chance_2 = dict[nag_2][2]
                for nag_3 in dict:
                    if nag_3 not in nags:
                        nags.append(nag_3)
                        pp_pool_perc_3 = dict[nag_3][0] / pool_size
                        win_chance_3 = dict[nag_3][1]
                        place_chance_3 = dict[nag_3][2]
                        for nag_4 in dict:
                            if nag_4 not in nags:
                                pp_pool_perc_4 = dict[nag_4][0] / pool_size
                                win_chance_4 = dict[nag_4][1]
                                place_chance_4 = dict[nag_4][2]
                                chance_1_2_3_4 = win_chance_1 * (win_chance_2 / (1 - win_chance_1)) * (win_chance_3 / (1 - win_chance_1 - win_chance_2)) * (win_chance_4 / (1 - win_chance_1 - win_chance_2 - win_chance_3))
                                chance_1_2_4_3 = win_chance_1 * (win_chance_2 / (1 - win_chance_1)) * (win_chance_4 / (1 - win_chance_1 - win_chance_2)) * (win_chance_3 / (1 - win_chance_1 - win_chance_2 - win_chance_4))
                                chance_1_3_2_4 = win_chance_1 * (win_chance_3 / (1 - win_chance_1)) * (win_chance_2 / (1 - win_chance_1 - win_chance_3)) * (win_chance_4 / (1 - win_chance_1 - win_chance_3 - win_chance_2))
                                chance_1_3_4_2 = win_chance_1 * (win_chance_3 / (1 - win_chance_1)) * (win_chance_4 / (1 - win_chance_1 - win_chance_3)) * (win_chance_2 / (1 - win_chance_1 - win_chance_3 - win_chance_4))
                                chance_1_4_2_3 = win_chance_1 * (win_chance_4 / (1 - win_chance_1)) * (win_chance_2 / (1 - win_chance_1 - win_chance_4)) * (win_chance_3 / (1 - win_chance_1 - win_chance_4 - win_chance_2))
                                chance_1_4_3_2 = win_chance_1 * (win_chance_4 / (1 - win_chance_1)) * (win_chance_3 / (1 - win_chance_1 - win_chance_4)) * (win_chance_2 / (1 - win_chance_1 - win_chance_4 - win_chance_3))
                                chance_2_1_3_4 = win_chance_2 * (win_chance_1 / (1 - win_chance_2)) * (win_chance_3 / (1 - win_chance_2 - win_chance_1)) * (win_chance_4 / (1 - win_chance_2 - win_chance_1 - win_chance_3))
                                chance_2_1_4_3 = win_chance_2 * (win_chance_1 / (1 - win_chance_2)) * (win_chance_4 / (1 - win_chance_2 - win_chance_1)) * (win_chance_3 / (1 - win_chance_2 - win_chance_1 - win_chance_4))
                                chance_2_3_1_4 = win_chance_2 * (win_chance_3 / (1 - win_chance_2)) * (win_chance_1 / (1 - win_chance_2 - win_chance_3)) * (win_chance_4 / (1 - win_chance_2 - win_chance_3 - win_chance_1))
                                chance_2_3_4_1 = win_chance_2 * (win_chance_3 / (1 - win_chance_2)) * (win_chance_4 / (1 - win_chance_2 - win_chance_3)) * (win_chance_1 / (1 - win_chance_2 - win_chance_3 - win_chance_4))
                                chance_2_4_1_3 = win_chance_2 * (win_chance_4 / (1 - win_chance_2)) * (win_chance_1 / (1 - win_chance_2 - win_chance_4)) * (win_chance_3 / (1 - win_chance_2 - win_chance_4 - win_chance_1))
                                chance_2_4_3_1 = win_chance_2 * (win_chance_4 / (1 - win_chance_2)) * (win_chance_3 / (1 - win_chance_2 - win_chance_4)) * (win_chance_1 / (1 - win_chance_2 - win_chance_4 - win_chance_3))
                                chance_3_2_1_4 = win_chance_3 * (win_chance_2 / (1 - win_chance_3)) * (win_chance_1 / (1 - win_chance_3 - win_chance_2)) * (win_chance_4 / (1 - win_chance_3 - win_chance_2 - win_chance_1))
                                chance_3_2_4_1 = win_chance_3 * (win_chance_2 / (1 - win_chance_3)) * (win_chance_4 / (1 - win_chance_3 - win_chance_2)) * (win_chance_1 / (1 - win_chance_3 - win_chance_2 - win_chance_4))
                                chance_3_1_2_4 = win_chance_3 * (win_chance_1 / (1 - win_chance_3)) * (win_chance_2 / (1 - win_chance_3 - win_chance_1)) * (win_chance_4 / (1 - win_chance_3 - win_chance_1 - win_chance_2))
                                chance_3_1_4_2 = win_chance_3 * (win_chance_1 / (1 - win_chance_3)) * (win_chance_4 / (1 - win_chance_3 - win_chance_1)) * (win_chance_2 / (1 - win_chance_3 - win_chance_1 - win_chance_4))
                                chance_3_4_2_1 = win_chance_3 * (win_chance_4 / (1 - win_chance_3)) * (win_chance_2 / (1 - win_chance_3 - win_chance_4)) * (win_chance_1 / (1 - win_chance_3 - win_chance_4 - win_chance_2))
                                chance_3_4_1_2 = win_chance_3 * (win_chance_4 / (1 - win_chance_3)) * (win_chance_1 / (1 - win_chance_3 - win_chance_4)) * (win_chance_2 / (1 - win_chance_3 - win_chance_4 - win_chance_1))
                                chance_4_2_3_1 = win_chance_4 * (win_chance_2 / (1 - win_chance_4)) * (win_chance_3 / (1 - win_chance_4 - win_chance_2)) * (win_chance_1 / (1 - win_chance_4 - win_chance_2 - win_chance_3))
                                chance_4_2_1_3 = win_chance_4 * (win_chance_2 / (1 - win_chance_4)) * (win_chance_1 / (1 - win_chance_4 - win_chance_2)) * (win_chance_3 / (1 - win_chance_4 - win_chance_2 - win_chance_1))
                                chance_4_3_2_1 = win_chance_4 * (win_chance_3 / (1 - win_chance_4)) * (win_chance_2 / (1 - win_chance_4 - win_chance_3)) * (win_chance_1 / (1 - win_chance_4 - win_chance_3 - win_chance_2))
                                chance_4_3_1_2 = win_chance_4 * (win_chance_3 / (1 - win_chance_4)) * (win_chance_1 / (1 - win_chance_4 - win_chance_3)) * (win_chance_2 / (1 - win_chance_4 - win_chance_3 - win_chance_1))
                                chance_4_1_2_3 = win_chance_4 * (win_chance_1 / (1 - win_chance_4)) * (win_chance_2 / (1 - win_chance_4 - win_chance_1)) * (win_chance_3 / (1 - win_chance_4 - win_chance_1 - win_chance_2))
                                chance_4_1_3_2 = win_chance_4 * (win_chance_1 / (1 - win_chance_4)) * (win_chance_3 / (1 - win_chance_4 - win_chance_1)) * (win_chance_2 / (1 - win_chance_4 - win_chance_1 - win_chance_3))
                                try:
                                    pp_pool_value = 1 / (pp_pool_perc_1 + pp_pool_perc_2 + pp_pool_perc_3 + pp_pool_perc_4) * \
                                        (chance_1_2_3_4 + chance_1_2_4_3 + chance_1_3_2_4 + chance_1_3_4_2 + chance_1_4_2_3 + chance_1_4_3_2 + \
                                            chance_2_1_3_4 + chance_2_1_4_3 + chance_2_3_1_4 + chance_2_3_4_1 + chance_2_4_1_3 + chance_2_4_3_1 + \
                                            chance_3_2_1_4 + chance_3_2_4_1 + chance_3_1_2_4 + chance_3_1_4_2 + chance_3_4_2_1 + chance_3_4_1_2 + \
                                            chance_4_2_3_1 + chance_4_2_1_3 + chance_4_3_2_1 + chance_4_3_1_2 + chance_4_1_2_3 + chance_4_1_3_2)
                                except:
                                    pp_pool_value = 0
                                pp_pool_value_1 += pp_pool_value
        result[nag_1] = [pp_pool_perc_1, pp_pool_value_1]
    return result
