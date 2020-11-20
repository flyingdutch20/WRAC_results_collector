import os
import rp
"""
basepath = 'mtg'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        rp.Meeting = \


            load_meeting_and_collect_results(os.path.join(basepath, entry), False, True)
"""

"""
def load_meeting_and_collect_results(filename, collect_pp, results):
    with open(filename, "rb") as mtgfile:
        mtg = None
        try:
            mtg = pickle.load(mtgfile)
        except Exception:
            print(f"Can't unpickle {filename}")
        if isinstance(mtg, Meeting):
            print("We have a meeting")
            mtg.collect_results(collect_pp, results)
            print(f"Saving {mtg.name}")
            mtg.writemtg()
"""

my_mtg = rp.Meeting()
my_mtg = rp.unpickle_mtg("2020-10-17-ascot.picle")