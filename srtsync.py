#!/usr/bin/python

""" Sync SubRip (SRT) subtitle files

Author: Gaetan Covelli <gaetan.covelli@gmail.com>
License: MIT

"""

import re
import sys
import getopt


def _to_seconds(raw_time):
    """ Converts hh:mm:ss,ms time format to seconds. """
    hours, mins, secs = raw_time.split(':')
    return int(hours) * 3600 + int(mins) * 60 + float(secs.replace(',', '.'))


def _to_hhmmss(seconds):
    """ Converts seconds to hh:mm:ss,ms time format """
    total_secs = float(seconds)
    hours = int(total_secs / 3600)
    mins = int((total_secs - (hours * 3600)) / 60)
    secs = total_secs - (hours * 3600) - (mins * 60)

    hours = '{:02d}'.format(hours)
    mins = '{:02d}'.format(mins)
    secs = '{:.3f}'.format(secs)

    if float(secs) < 10:
        secs = '0{}'.format(secs)

    return '{}:{}:{}'.format(hours, mins, secs.replace('.', ','))


def _sync_section(match, time_diff):
    """ Sync a subtitle section """
    curr_time = _to_seconds(match.group(0))
    synced_time = curr_time + time_diff

    if synced_time < 0:
        synced_time = 0

    return _to_hhmmss(synced_time)


def sync(input_file, output_file, *timings):
    """ Sync the subtitles file """
    if len(timings) == 1:
        diff = timings[0]
        diff /= 1000.0
    elif len(timings) == 2:
        diff = _to_seconds(timings[1]) - _to_seconds(timings[0])
    else:
        raise Exception, "Invalid timings: " + str(timings)

    input_file = open(input_file, 'r')
    output_file = open(output_file, 'w')
    regex = r'(\d{2}:\d{2}:\d{2},\d{3})'

    for curr_line in input_file:
        new_line = re.sub(
            regex,
            lambda line: _sync_section(line, diff),
            curr_line.rstrip('\n'))
        output_file.write(new_line)

    input_file.close()
    output_file.close()


def main(argv):
    """ Sync the subtitles from the command line """
    usage = ('Usage: srtsync.py -i <inputfile> -o <outputfile>'
             ' -t <time_in_ms> \n'
             'Or: srtsync.py -i <inputfile> -o <outputfile>'
             ' -c <current-time> -e <expected-time>')
    options = 'hi:o:t:c:e:'
    long_options = [
        'input=',
        'output=',
        'time-diff=',
        'current-time=',
        'expected-time='
    ]
    input_file = ''
    output_file = ''
    time_diff = None
    current_time = None
    expected_time = None

    try:
        opts, _ = getopt.getopt(argv, options, long_options)
    except getopt.GetoptError:
        print usage
        sys.exit(2)

    if len(opts) == 0:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ('-i', '--input'):
            input_file = arg
        elif opt in ('-o', '--output'):
            output_file = arg
        elif opt in ('-t', '--time-diff'):
            time_diff = float(arg)
        elif opt in ('-c', '--current-time'):
            current_time = arg
        elif opt in ('-e', '--expected-time'):
            expected_time = arg

    files_present = input_file and output_file
    timings_present = time_diff or (current_time and expected_time)

    if not files_present or not timings_present:
        print usage
        sys.exit(2)

    if current_time and expected_time:
        sync(input_file, output_file, current_time, expected_time)
    else:
        sync(input_file, output_file, time_diff)

if __name__ == '__main__':
    main(sys.argv[1:])
    