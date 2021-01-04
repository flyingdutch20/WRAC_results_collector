# calculate pp value for a dict nag -> [pp pool, place chance]
# return a dictionary nag -> value

def set_pool_size(in_dict):
    global pool_size
    pool_size = 0
    for x in in_dict.values():
        pool_size += x[0]
    return pool_size

def remove_nr(in_dict):
    my_dict = {}
    for nag in in_dict:
        if in_dict[nag][3] > 0:
            my_dict[nag] = in_dict[nag]
    return my_dict

def calc_pp_value(in_dict, places):
    my_pool_size = set_pool_size(in_dict)
    if my_pool_size == 0:
        return {}
    my_dict = remove_nr(in_dict)
    if places == 1:
        return calc_pp_value_1(my_dict)
    elif places == 2:
        return calc_pp_value_2(my_dict)
    elif places == 3:
        return calc_pp_value_3(my_dict)
    elif places == 4:
        return calc_pp_value_4(my_dict)
    else:
        return {}

def calc_pp_value_1(my_dict):
    result = {}
    for nag_1 in my_dict:
        pp_pool_perc_1 = my_dict[nag_1][0]/pool_size
        win_chance_1 = my_dict[nag_1][1]
        place_chance_1 = my_dict[nag_1][2]
        try:
            pp_pool_value_1 = (1 / pp_pool_perc_1) * win_chance_1
        except:
            pp_pool_value_1 = 0
        result[nag_1] = [pp_pool_perc_1, pp_pool_value_1]
    return result

def calc_pp_value_2(my_dict):
    result = {}
    for nag_1 in my_dict:
        pp_pool_perc_1 = my_dict[nag_1][0]/pool_size
        win_chance_1 = my_dict[nag_1][1]
        place_chance_1 = my_dict[nag_1][2]
        pp_pool_value_1 = 0
        nags = [nag_1]
        for nag_2 in my_dict:
            if nag_2 not in nags:
                pp_pool_perc_2 = my_dict[nag_2][0] / pool_size
                win_chance_2 = my_dict[nag_2][1]
                place_chance_2 = my_dict[nag_2][2]
                chance_1_2 = win_chance_1 * (win_chance_2 / (1 - win_chance_1))
                chance_2_1 = win_chance_2 * (win_chance_1 / (1 - win_chance_2))
                try:
                    pp_pool_value = (1 / (pp_pool_perc_1 + pp_pool_perc_2)) * \
                                    (chance_1_2 + chance_2_1)
                except:
                    pp_pool_value = 0
                pp_pool_value_1 += pp_pool_value
        result[nag_1] = [pp_pool_perc_1, (pp_pool_value_1 * (1/2))]
    return result

def calc_pp_value_3(my_dict):
    result = {}
    for nag_1 in my_dict:
        pp_pool_perc_1 = my_dict[nag_1][0]/pool_size
        win_chance_1 = my_dict[nag_1][1]
        pp_pool_value_1 = 0
        dict_2 = my_dict.copy()
        dict_2.pop(nag_1)
        for nag_2 in dict_2:
            pp_pool_perc_2 = my_dict[nag_2][0] / pool_size
            win_chance_2 = my_dict[nag_2][1]
            dict_3 = dict_2.copy()
            dict_3.pop(nag_2)
            for nag_3 in dict_3:
                pp_pool_perc_3 = my_dict[nag_3][0] / pool_size
                win_chance_3 = my_dict[nag_3][1]
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
        result[nag_1] = [pp_pool_perc_1, (pp_pool_value_1 * (1/3))]
    return result

def calc_pp_value_4(my_dict):
    result = {}
    for nag_1 in my_dict:
        pp_pool_perc_1 = my_dict[nag_1][0]/pool_size
        win_chance_1 = my_dict[nag_1][1]
        pp_pool_value_1 = 0
        dict_2 = my_dict.copy()
        dict_2.pop(nag_1)
        for nag_2 in dict_2:
            pp_pool_perc_2 = my_dict[nag_2][0] / pool_size
            win_chance_2 = my_dict[nag_2][1]
            dict_3 = dict_2.copy()
            dict_3.pop(nag_2)
            for nag_3 in dict_3:
                pp_pool_perc_3 = my_dict[nag_3][0] / pool_size
                win_chance_3 = my_dict[nag_3][1]
                dict_4 = dict_3.copy()
                dict_4.pop(nag_3)
                for nag_4 in dict_4:
                    pp_pool_perc_4 = my_dict[nag_4][0] / pool_size
                    win_chance_4 = my_dict[nag_4][1]
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
                    tot_pp_pool_perc = pp_pool_perc_1 + pp_pool_perc_2 + pp_pool_perc_3 + pp_pool_perc_4
                    tot_chance_1 = chance_1_2_3_4 + chance_1_2_4_3 + chance_1_3_2_4 + chance_1_3_4_2 + chance_1_4_2_3 + chance_1_4_3_2
                    tot_chance_2 = chance_2_1_3_4 + chance_2_1_4_3 + chance_2_3_1_4 + chance_2_3_4_1 + chance_2_4_1_3 + chance_2_4_3_1
                    tot_chance_3 = chance_3_2_1_4 + chance_3_2_4_1 + chance_3_1_2_4 + chance_3_1_4_2 + chance_3_4_2_1 + chance_3_4_1_2
                    tot_chance_4 = chance_4_2_3_1 + chance_4_2_1_3 + chance_4_3_2_1 + chance_4_3_1_2 + chance_4_1_2_3 + chance_4_1_3_2
                    sum_tot_chance = tot_chance_1 + tot_chance_2 + tot_chance_3 + tot_chance_4
                    try:
                        pp_pool_value = 1 / tot_pp_pool_perc * sum_tot_chance
                    except:
                        pp_pool_value = 0
                    pp_pool_value_1 += pp_pool_value
        result[nag_1] = [pp_pool_perc_1, (pp_pool_value_1 * (1/4))]
    return result
