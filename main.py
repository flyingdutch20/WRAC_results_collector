import argparse
import rp


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='WRAC running and tri results collector',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('weeks',
                        type=int,
                        default=1,
                        help='Number of weeks to collect')

    parser.add_argument('-t',
                        '--test',
                        help="Don't send the results out",
                        action='store_false')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    test = args.test
    weeks = args.weeks
    rp.read_racingpost_index(test, weeks)
