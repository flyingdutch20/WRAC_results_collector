import argparse
import rp


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

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    tote = args.tote
    results = args.results
    meeting = args.meeting.lower()
    rp.read_racingpost_index(meeting, tote, results)
