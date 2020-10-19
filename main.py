import argparse
import rp

class Meeting:
    def __init__(self):
        self.name = ""
        self.race_date = ""
        self.start = ""
        self.type = ""
        self.going = ""
        self.stalls = ""
        self.pp_pool = 0
        self.pp_div = 0
        self.races = []

class Racecard:
    def __init__(self):
        self.mtgname = ""
        self.name = ""
        self.rp_id = ""
        self.rp_url = ""
        self.race_time = ""
        self.race_class = ""
        self.distance = ""
        self.field = ""
        self.verdict = ""
        self.pp_fav = 0
        self.pp_fav_perc = ""
        self.pp_nr = 0
        self.pp_pool = 0
        self.nags = {}
        self.totepp_url = ""
        self.leg = 0

class Nag:
    def __init__(self):
        self.name = ""
        self.rp_id = ""
        self.no = ""
        self.draw = ""
        self.lastrun = ""
        self.form = ""
        self.age = ""
        self.jockey = ""
        self.trainer = ""
        self.ts = ""
        self.rpr = ""
        self.rp_comment = ""
        self.rp_forecast = 0
        self.bet365_odds = []
        self.best_odds = []
        self.bf_odds = []
        self.result = ""
        self.sp = 0
        self.fav = ""
        self.race_comment = ""
        self.pp_pool = 0
        self.pp_pool_perc = ""
        self.placed = False

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Racecard and Placepot information collector',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-t',
                        '--tote',
                        help="Don't collect Tote pp data",
                        action='store_false')

    parser.add_argument('-r',
                        '--results',
                        help="Don't collect Racingpost results",
                        action='store_false')

    parser.add_argument('-m',
                        '--meeting',
                        metavar='str',
                        type=str,
                        default='',
                        help='Meeting to collect')

    parser.add_argument('-f',
                        '--filename',
                        metavar='str',
                        type=str,
                        default='',
                        help='Upload picle meeting file to add results')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    tote = args.tote
    results = args.results
    meeting = args.meeting.lower()
    filename = args.filename
    if args.filename:
        rp.load_meeting_and_collect_results(filename, tote, results)
    else:
        rp.read_racingpost_index(meeting, tote, results)
