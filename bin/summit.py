#!/usr/bin/env python

#
# Copyright (c) 2018 Palo Alto Networks, Inc. <techbizdev@paloaltonetworks.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# This summit is in the cloud.

from __future__ import print_function
import datetime
import getopt
import inspect
import json
import logging as logging_
import os
import pprint
import sys
try:
    import jmespath
    from jmespath import exceptions
    have_jmespath = True
except ImportError:
    have_jmespath = False
try:
    import arrow
    have_arrow = True
except ImportError:
    have_arrow = False

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir)]

from pancloud import HTTPClient, LoggingService, EventService, \
    DirectorySyncService, __version__

INDENT = 2
LOGGING_SERVICE_EPOCH = 1504224000  # 2017-09-01T00:00:00+00:00
DEFAULT_EVENT_CHANNEL_ID = 'EventFilter'
debug = 0


def main():
    options = parse_opts()

    if options['debug']:
        logger = logging_.getLogger()
        logger.setLevel(logging_.DEBUG)
        log_format = '%(message)s'
        handler = logging_.StreamHandler()
        formatter = logging_.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if (sum(bool(x) for x in [options['logging_api'],
                              options['event_api'],
                              options['directory_sync_api']]) > 1):
        print('Only a single Service API request allowed',
              file=sys.stderr)
        sys.exit(1)

    if options['logging_api']:
        logging(options)

    if options['event_api']:
        if options['id'] is None:
            options['id'] = DEFAULT_EVENT_CHANNEL_ID
        event(options)

    if options['directory_sync_api']:
        directory_sync(options)

    sys.exit(0)


def logging(options):
    def query(api, options):
        action = inspect.stack()[0][3]

        x = options['R1_obj'].copy()
        if options['start_seconds']:
            x['startTime'] = options['start_seconds']
        if options['end_seconds']:
            x['endTime'] = options['end_seconds']

        if options['debug'] > 2:
            print(pprint.pformat(x, indent=INDENT),
                  file=sys.stderr)

        try:
            r = api.query(data=x, **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def poll(api, options):
        action = inspect.stack()[0][3]

        try:
            r = api.poll(query_id=options['id'],
                         sequence_no=options['seq'],
                         params=options['R1_obj'],
                         **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def xpoll(api, options):
        action = inspect.stack()[0][3]

        try:
            for x in api.xpoll(query_id=options['id'],
                               sequence_no=options['seq'],
                               delete_query=options['delete'],
                               params=options['R1_obj'],
                               **options['R2_obj']):
                print_response_body(options, x)

        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    def delete(api, options):
        action = inspect.stack()[0][3]

        try:
            r = api.delete(query_id=options['id'],
                           **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def write(api, options):
        action = inspect.stack()[0][3]
        print(action, 'not implemented')

    action = inspect.stack()[0][3]

    try:
        if options['http_client']:
            session = HTTPClient(**options['R3_obj'])
            api = LoggingService(session=session, **options['R0_obj'])
        else:
            api = LoggingService(**options['R0_obj'])
    except Exception as e:
        print_exception(action, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['query']:
        query(api, options)

    if options['poll']:
        poll(api, options)

    if options['xpoll']:
        try:
            xpoll(api, options)
        except KeyboardInterrupt:
            sys.exit(1)

    if options['delete'] and not options['xpoll']:
        delete(api, options)

    if options['write']:
        write(api, options)


def event(options):
    def generic(api, options, func, action):
        try:
            r = func(channel_id=options['id'],
                     **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def set_filters(api, options):
        action = inspect.stack()[0][3]

        try:
            r = api.set_filters(channel_id=options['id'],
                                data=options['R1_obj'],
                                **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def get_filters(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.get_filters, action)

    def xpoll(api, options):
        action = inspect.stack()[0][3]

        try:
            for x in api.xpoll(channel_id=options['id'],
                               data=options['R1_obj'],
                               ack=options['ack'],
                               follow=options['follow'],
                               **options['R2_obj']):
                print('%s:' % action, end='', file=sys.stderr)
                event_print_status(options, [x])
                print(file=sys.stderr)
                print_response_body(options, x)
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    def poll(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.poll, action)

    def ack(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.ack, action)

    def nack(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.nack, action)

    action = inspect.stack()[0][3]

    try:
        if options['http_client']:
            session = HTTPClient(**options['R3_obj'])
            api = EventService(session=session, **options['R0_obj'])
        else:
            api = EventService(**options['R0_obj'])
    except Exception as e:
        print_exception(action, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['set']:
        set_filters(api, options)

    if options['get']:
        get_filters(api, options)

    if options['poll']:
        poll(api, options)

    if options['xpoll']:
        try:
            xpoll(api, options)
        except KeyboardInterrupt:
            sys.exit(1)

    if options['ack'] and not options['xpoll']:
        ack(api, options)

    if options['nack']:
        nack(api, options)


def directory_sync(options):
    def generic(api, options, func, action):
        try:
            r = func(**options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def query(api, options):
        action = inspect.stack()[0][3]

        try:
            r = api.query(object_class=options['id'],
                          data=options['R1_obj'],
                          **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def count(api, options):
        action = inspect.stack()[0][3]

        try:
            r = api.count(object_class=options['id'],
                          **options['R2_obj'])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def domains(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.domains, action)

    def attributes(api, options):
        action = inspect.stack()[0][3]
        generic(api, options, api.attributes, action)

    action = inspect.stack()[0][3]

    try:
        if options['http_client']:
            session = HTTPClient(**options['R3_obj'])
            api = DirectorySyncService(session=session, **options['R0_obj'])
        else:
            api = DirectorySyncService(**options['R0_obj'])
    except Exception as e:
        print_exception(action, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['query']:
        query(api, options)

    if options['count']:
        count(api, options)

    if options['domains']:
        domains(api, options)

    if options['attributes']:
        attributes(api, options)


def print_exception(action, e):
    print('%s:' % action, end='', file=sys.stderr)
    print(' %s:' % e.__class__.__name__, end='', file=sys.stderr)
    print(' "%s"' % e, file=sys.stderr)


def print_status(action, r, options):
    print('%s:' % action, end='', file=sys.stderr)

    if r.status_code is not None:
        print(' %s' % r.status_code, end='', file=sys.stderr)
    if r.reason is not None:
        print(' %s' % r.reason, end='', file=sys.stderr)
    if r.headers is not None:
        print(' %s' % r.headers.get('content-length'),
              end='', file=sys.stderr)
    try:
        x = r.json()
    except ValueError:
        print(file=sys.stderr)
        return

    if 'errorCode' in x:
        print(": %s" % x['errorCode'], end='', file=sys.stderr)
    if 'errorMessage' in x:
        print(": '%s'" % x['errorMessage'], end='', file=sys.stderr)

    if (options['logging_api']):
        logging_print_status(options, x)
    if (options['event_api']):
        event_print_status(options, x)
    if (options['directory_sync_api']):
        directory_sync_print_status(options, x)

    print(file=sys.stderr)


def logging_print_status(options, x):
    if 'queryStatus' in x:
        print(" queryStatus=%s" % x['queryStatus'], end='',
              file=sys.stderr)
        # XXX validate expected
        if options['query'] or options['poll']:
            if x['queryStatus'] not in ['RUNNING', 'FINISHED',
                                        'JOB_FINISHED', 'JOB_FAILED']:
                print("(INVALID)", end='', file=sys.stderr)
    if 'queryId' in x:
        print(" queryId=%s" % x['queryId'], end='', file=sys.stderr)
    if 'sequenceNo' in x:
        print(" sequenceNo=%s" % x['sequenceNo'], end='', file=sys.stderr)
    try:
        v = x['result']['esResult']['size']
    except (TypeError, KeyError):
        pass
    else:
        print(' size=%d' % v, end='', file=sys.stderr)


def event_print_status(options, x):
    for ev in x:
        if 'logType' in ev:
            print(' %s' % ev['logType'], end='', file=sys.stderr)
        if 'event' in ev:
            print('[size=%d]' % len(ev['event']), end='', file=sys.stderr)
            if options['debug'] > 0:
                k = 'receive_time'
                try:
                    seconds = ev['event'][-1][k]
                    t = datetime.datetime.utcfromtimestamp(seconds)
                    print(' %s' % t, end='', file=sys.stderr)
                except (IndexError, KeyError):
                    pass

                t0 = datetime.datetime.utcfromtimestamp(0)
                seq0 = 0
                try:
                    for log in ev['event']:
                        t1 = datetime.datetime.utcfromtimestamp(log[k])
                        seq1 = log['seqno']
                        if t0 > t1:
                            # XXX logs not in chronological order
                            print('\nWarning: %s: %s %s > %s %s' %
                                  (k, seq0, t0, seq1, t1),
                                  end='', file=sys.stderr)
                        t0 = t1
                        seq0 = seq1
                except KeyError:
                    pass


def directory_sync_print_status(options, x):
    if 'count' in x:
        print(" count=%d" % x['count'], end='', file=sys.stderr)
    if 'pageNumber' in x:
        print(" pageNumber=%d" % x['pageNumber'], end='', file=sys.stderr)
    if 'pageSize' in x:
        print(" pageSize=%d" % x['pageSize'], end='', file=sys.stderr)
    if 'unreadResults' in x:
        print(" unreadResults=%d" % x['unreadResults'], end='',
              file=sys.stderr)


def print_response(r, options):
    if options['debug'] > 2:
        print(pprint.pformat(dict(r.headers), indent=INDENT),
              file=sys.stderr)
        print(r.text, file=sys.stderr)

    if r.text is None or r.headers is None:
        return

    x = r.headers.get('content-type')
    if x is None:
        return

    if x.startswith('application/json'):
        try:
            obj = r.json()
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        print_response_body(options, obj)
    else:
        print('WARNING: Response Content-Type:', x, file=sys.stderr)


def print_response_body(options, x):
        if options['jmespath'] is not None:
            x = jmespath_search(options['jmespath'], x)

        if options['print_json']:
            print_json(x)

        if options['print_python']:
            print_python(x)


def exit_for_http_status(r):
    if r.status_code is not None:
        if not (200 <= r.status_code < 300):
            sys.exit(1)
        else:
            return

    print('status_code:', r.status_code, file=sys.stderr)
    sys.exit(1)


def print_python(obj):
    print(pprint.pformat(obj, indent=INDENT))


def print_json(obj):
    print(json.dumps(obj, sort_keys=True, indent=INDENT,
                     separators=(',', ': ')))


def jmespath_search(expression, obj):
    try:
        x = jmespath.search(expression, obj)
    except exceptions.JMESPathError as e:
        print('JMESPath %s: %s' % (e.__class__.__name__, e), file=sys.stderr)
        sys.exit(1)

    return x


def process_arg(x):
    stdin_char = '-'

    if x == stdin_char:
        lines = sys.stdin.readlines()
    else:
        try:
            f = open(x)
            lines = f.readlines()
            f.close()
        except IOError:
            lines = [x]

    if debug > 1:
        print(pprint.pformat(lines, indent=INDENT), file=sys.stderr)

    lines = ''.join(lines)
    return lines


def process_json_args(args, init=None):
        obj = init or {}
        for r in args:
            try:
                x = json.loads(r)
            except ValueError as e:
                print('%s: %s' % (e, r), file=sys.stderr)
                sys.exit(1)
            obj.update(x)

        # XXX used for debug only
        try:
            json_arg = json.dumps(obj, indent=INDENT)
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        if debug > 1:
            print(pprint.pformat(obj, indent=INDENT), file=sys.stderr)
            print(json_arg, file=sys.stderr)

        return obj


def process_time(x):
    try:
        seconds = int(x)
    except ValueError as e:
        if not have_arrow:
            print('%s: %s' % (str(x), e), file=sys.stderr)
            print('Install arrow module for non Unix epoch time support: '
                  'http://arrow.readthedocs.io/', file=sys.stderr)
            sys.exit(1)

        try:
            t = arrow.get(x)
        except arrow.parser.ParserError as e:
            print('%s: %s' % (str(x), e), file=sys.stderr)
            sys.exit(1)

        seconds = t.timestamp
        if debug > 1:
            print('time %d: %s' % (seconds, t), file=sys.stderr)

    else:
        try:
            t = datetime.datetime.utcfromtimestamp(seconds)
        except ValueError as e:
            print('%s: %s' % (str(x), e), file=sys.stderr)
            sys.exit(1)

        if debug > 1:
            print('time %d: %s' % (seconds, t), file=sys.stderr)

    if seconds < LOGGING_SERVICE_EPOCH:
        t0 = datetime.datetime.utcfromtimestamp(LOGGING_SERVICE_EPOCH)
        t = datetime.datetime.utcfromtimestamp(seconds)
        print('Warning: "%s" < logging service epoch "%s"' % (t, t0),
              file=sys.stderr)

    return seconds


def parse_opts():
    options = {
        'http_client': False,
        'logging_api': False,
        'directory_sync_api': False,
        'event_api': False,
        'delete': False,
        'poll': False,
        'xpoll': False,
        'query': False,
        'write': False,
        'start': None,
        'start_seconds': None,
        'id': None,
        'seq': 0,
        'end': None,
        'end_seconds': None,
        'set': False,
        'get': False,
        'ack': False,
        'nack': False,
        'follow': False,
        'count': False,
        'domains': False,
        'attributes': False,
        #
        'R0': [],
        'R0_obj': {},
        'R1': [],
        'R1_obj': {},
        'R2': [],
        'R2_obj': {},
        'R3': [],
        'R3_obj': {},
        'jmespath': None,
        'print_python': False,
        'print_json': False,
        'debug': 0,
        }

    short_options = 'HLDEJ:pj'
    long_options = [
        'delete', 'poll', 'xpoll', 'query', 'write',
        'start=', 'end=',
        'id=', 'seq=',
        'set', 'get', 'ack', 'nack', 'follow',
        'count', 'domains', 'attributes',
        'R0=', 'R1=', 'R2=', 'R3=',
        'debug=', 'version', 'help',
    ]

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   short_options,
                                   long_options)
    except getopt.GetoptError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    for opt, arg in opts:
        if False:
            pass
        elif opt == '-H':
            options['http_client'] = True
        elif opt == '-L':
            options['logging_api'] = True
        elif opt == '-D':
            options['directory_sync_api'] = True
        elif opt == '-E':
            options['event_api'] = True
        elif opt == '--delete':
            options['delete'] = True
        elif opt == '--poll':
            options['poll'] = True
        elif opt == '--xpoll':
            options['xpoll'] = True
        elif opt == '--query':
            options['query'] = True
        elif opt == '--write':
            options['write'] = True
        elif opt == '--start':
            options['start'] = arg
            options['start_seconds'] = process_time(arg)
        elif opt == '--end':
            options['end'] = arg
            options['end_seconds'] = process_time(arg)
        elif opt == '--id':
            options['id'] = arg
        elif opt == '--seq':
            options['seq'] = arg
        elif opt == '--set':
            options['set'] = True
        elif opt == '--get':
            options['get'] = True
        elif opt == '--ack':
            options['ack'] = True
        elif opt == '--nack':
            options['nack'] = True
        elif opt == '--follow':
            options['follow'] = True
        elif opt == '--count':
            options['count'] = True
        elif opt == '--domains':
            options['domains'] = True
        elif opt == '--attributes':
            options['attributes'] = True
        elif opt == '--R0':
            options['R0'].append(process_arg(arg))
        elif opt == '--R1':
            options['R1'].append(process_arg(arg))
        elif opt == '--R2':
            options['R2'].append(process_arg(arg))
        elif opt == '--R3':
            options['R3'].append(process_arg(arg))
        elif opt == '-J':
            if not have_jmespath:
                print('Install JMESPath for -J support: http://jmespath.org/',
                      file=sys.stderr)
                sys.exit(1)
            options['jmespath'] = arg
        elif opt == '-p':
            options['print_python'] = True
        elif opt == '-j':
            options['print_json'] = True
        elif opt == '--debug':  # XXX positional
            try:
                options['debug'] = int(arg)
                if options['debug'] < 0:
                    raise ValueError
            except ValueError:
                print('Invalid debug:', arg, file=sys.stderr)
                sys.exit(1)
            if options['debug'] > 3:
                print('Maximum debug level is 3', file=sys.stderr)
                sys.exit(1)
            global debug
            debug = options['debug']
        elif opt == '--version':
            print('pancloud', __version__)
            sys.exit(0)
        elif opt == '--help':
            usage()
            sys.exit(0)
        else:
            assert False, 'unhandled option %s' % opt

    headers = None
    if 'ACCESS_TOKEN' in os.environ:
        headers = {
            'Authorization': 'Bearer %s' % os.environ['ACCESS_TOKEN'],
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    for x in ['R0', 'R1', 'R2', 'R3']:
        if options[x]:
            init = None
            if x in ['R0', 'R3'] and headers is not None:
                init = {'headers': headers}
            options[x + '_obj'] = process_json_args(options[x], init)

    if options['debug'] > 2:
        s = pprint.pformat(options, indent=INDENT)
        print(s, file=sys.stderr)

    return options


def usage():
    usage = '''%s [options]
    -L                    Logging Service API request using
                          LoggingService() class
      --delete            delete logging query
      --poll              poll logging query results
      --xpoll             poll all logging query records
      --query             query logging records
      --write             write logging records (future)
      --start time        startTime
      --end time          endTime
      --id id             queryId
      --seq no            sequenceNo
    -E                    Event Service API request using
                          EventService() class
      --set               set event channel filters
      --get               get event channel filters
      --ack               move event read point to current
      --nack              move event read point to previous
      --poll              poll events
      --xpoll             poll all events until drained
                          (use --ack to ack after each poll)
      --follow            follow xpoll after drained: xpoll(follow=True)
      --id id             channelId (default: "%s")
    -D                    Directory Sync Service API request using
                          DirectorySyncService() class
      --query             query directory entries
      --count             get count of directory entries
      --domains           get directory domains
      --attributes        get directory attributes
      --id class          objectClass
    -H                    use HTTPClient() session
    --R0 json             service class constructor args (**kwargs)
    --R1 json             service class method body/QUERY_STRING (data/params)
    --R2 json             service class method args (**kwargs)
    --R3 json             HTTPClient() class constructor args (**kwargs)
                          (multiple --R[0123]'s allowed)
    -J expression         JMESPath expression for JSON response data
    -p                    print response in Python to stdout
    -j                    print response in JSON to stdout
    --debug level         enable debug level up to 3
    --version             display version
    --help                display usage
''' % (os.path.basename(sys.argv[0]), DEFAULT_EVENT_CHANNEL_ID)
    print(usage, end='')


if __name__ == '__main__':
    main()
