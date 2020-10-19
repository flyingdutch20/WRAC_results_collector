import os
import rp

basepath = 'mtg\\'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        rp.Meeting = rp.load_meeting_and_collect_results(basepath + entry, False, True)
