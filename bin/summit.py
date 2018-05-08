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

from pancloud import Credentials, HTTPClient, LoggingService, \
    EventService, DirectorySyncService, __version__

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

    if options['credentials']:
        credentials_ = credentials(options)
    else:
        credentials_ = None

    if options['http_client']:
        httpclient_ = httpclient(options, credentials_)
    else:
        httpclient_ = None

    if options['logging_api']:
        logging(options, httpclient_)

    if options['event_api']:
        if options['id'] is None:
            options['id'] = DEFAULT_EVENT_CHANNEL_ID
        event(options, httpclient_)

    if options['directory_sync_api']:
        directory_sync(options, httpclient_)

    sys.exit(0)


def credentials(options):
    def write_credentials(c, options):
        action = inspect.stack()[0][3]
        k = 'Credentials:write'

        R = options['R']
        try:
            c.write_credentials(**R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    action = inspect.stack()[0][3]
    k = 'Credentials'

    R = options['R']
    try:
        x = Credentials(**R['R0_obj'][k])
    except Exception as e:
        print_exception(action, e)
        sys.exit(1)

    if options['write']:
        write_credentials(x, options)

    return x


def httpclient(options, c):
    action = inspect.stack()[0][3]
    k = 'HTTPClient'

    R = options['R']
    try:
        x = HTTPClient(credentials=c,
                       **R['R0_obj'][k])
    except Exception as e:
        print_exception(action, e)
        sys.exit(1)

    return x


def logging(options, session):
    def query(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:query'

        R = options['R']
        x = R['R1_obj'][k].copy()
        if options['start_seconds']:
            x['startTime'] = options['start_seconds']
        if options['end_seconds']:
            x['endTime'] = options['end_seconds']

        if options['debug'] > 2:
            print(pprint.pformat(x, indent=INDENT),
                  file=sys.stderr)

        try:
            r = api.query(data=x, **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def poll(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:poll'

        R = options['R']
        try:
            r = api.poll(query_id=options['id'],
                         sequence_no=options['seq'],
                         params=R['R1_obj'][k],
                         **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def xpoll(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:poll'

        R = options['R']
        try:
            for x in api.xpoll(query_id=options['id'],
                               sequence_no=options['seq'],
                               delete_query=options['delete'],
                               params=R['R1_obj'][k],
                               **R['R2_obj'][k]):
                print_response_body(options, x)

        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    def delete(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:delete'

        R = options['R']
        try:
            r = api.delete(query_id=options['id'],
                           **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def write(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:write'

        R = options['R']
        print(action, 'not implemented')

    action = inspect.stack()[0][3]
    k = 'LoggingService'

    R = options['R']
    try:
        api = LoggingService(session=session,
                             **R['R0_obj'][k])
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


def event(options, session):
    def generic(api, options, func, action, k):
        R = options['R']
        try:
            r = func(channel_id=options['id'],
                     **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def set_filters(api, options):
        action = inspect.stack()[0][3]
        k = 'EventService:set_filters'

        R = options['R']
        try:
            r = api.set_filters(channel_id=options['id'],
                                data=R['R1_obj'][k],
                                **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def get_filters(api, options):
        action = inspect.stack()[0][3]
        k = 'EventService:get_filters'
        generic(api, options, api.get_filters, action, k)

    def xpoll(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:xpoll'

        R = options['R']
        try:
            for x in api.xpoll(channel_id=options['id'],
                               data=R['R1_obj'][k],
                               ack=options['ack'],
                               follow=options['follow'],
                               **R['R2_obj'][k]):
                print('%s:' % action, end='', file=sys.stderr)
                event_print_status(options, [x])
                print(file=sys.stderr)
                print_response_body(options, x)
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    def poll(api, options):
        action = inspect.stack()[0][3]
        k = 'LoggingService:poll'

        R = options['R']
        try:
            r = api.poll(channel_id=options['id'],
                         data=R['R1_obj'][k],
                         **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

    def ack(api, options):
        action = inspect.stack()[0][3]
        k = 'EventService:ack'
        generic(api, options, api.ack, action, k)

    def nack(api, options):
        action = inspect.stack()[0][3]
        k = 'EventService:nack'
        generic(api, options, api.nack, action, k)

    action = inspect.stack()[0][3]
    k = 'EventService'

    R = options['R']
    try:
        api = EventService(session=session,
                           **R['R0_obj'][k])
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


def directory_sync(options, session):
    def generic(api, options, func, action, k):
        R = options['R']
        try:
            r = func(**R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def query(api, options):
        action = inspect.stack()[0][3]
        k = 'DirectorySyncService:query'

        R = options['R']
        try:
            r = api.query(object_class=options['id'],
                          data=R['R1_obj'][k],
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def count(api, options):
        action = inspect.stack()[0][3]
        k = 'DirectorySyncService:count'

        R = options['R']
        try:
            r = api.count(object_class=options['id'],
                          params=R['R1_obj'][k],
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(action, e)
            sys.exit(1)

        print_status(action, r, options)
        print_response(r, options)
        exit_for_http_status(r)

    def domains(api, options):
        action = inspect.stack()[0][3]
        k = 'DirectorySyncService:domains'
        generic(api, options, api.domains, action, k)

    def attributes(api, options):
        action = inspect.stack()[0][3]
        k = 'DirectorySyncService:attributes'
        generic(api, options, api.attributes, action, k)

    action = inspect.stack()[0][3]
    k = 'DirectorySyncService'

    R = options['R']
    try:
        api = DirectorySyncService(session=session,
                                   **R['R0_obj'][k])
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

        if debug > 1 and obj:
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
    options_R = {
        # class init **kwargs
        'R0': {
            'Credentials': [],
            'HTTPClient': [],
            'LoggingService': [],
            'EventService': [],
            'DirectorySyncService': [],
        },
        # class method data/params
        # XXX can't have data and params
        'R1': {
            'LoggingService:query': [],
            'LoggingService:poll': [],
            'LoggingService:xpoll': [],

            'EventService:set_filters': [],
            'EventService:poll': [],
            'EventService:xpoll': [],

            'DirectorySyncService:query': [],
            'DirectorySyncService:count': [],
        },
        # class method **kwargs
        'R2': {
            'Credentials:write': [],

            'LoggingService:delete': [],
            'LoggingService:poll': [],
            'LoggingService:xpoll': [],
            'LoggingService:query': [],
            'LoggingService:write': [],

            'EventService:set_filters': [],
            'EventService:get_filters': [],
            'EventService:ack': [],
            'EventService:nack': [],
            'EventService:poll': [],
            'EventService:xpoll': [],

            'DirectorySyncService:query': [],
            'DirectorySyncService:count': [],
            'DirectorySyncService:domains': [],
            'DirectorySyncService:attributes': [],
        },
    }

    options = {
        'R': options_R,
        'credentials': False,
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
        'jmespath': None,
        'print_python': False,
        'print_json': False,
        'debug': 0,
        }

    def _options_R(k, last_c, last_m, arg):
        if k == 'R0':
            if last_c in options_R[k]:
                options_R[k][last_c].append(process_arg(arg))
            else:
                print('--%s has no class context' % k, file=sys.stderr)
                sys.exit(1)

        elif k in ['R1', 'R2']:
            x = '%s:%s' % (last_c, last_m)
            if x in options_R[k]:
                options_R[k][x].append(process_arg(arg))
            else:
                print('--%s has no class:method context: %s' % (k, x),
                      file=sys.stderr)
                sys.exit(1)

    short_options = 'CHLDEJ:pj'
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

    last_c = ''  # class
    last_m = ''  # method

    for opt, arg in opts:
        if False:
            pass
        elif opt == '-C':
            options['credentials'] = True
            last_c = 'Credentials'
        elif opt == '-H':
            options['http_client'] = True
            last_c = 'HTTPClient'
        elif opt == '-L':
            options['logging_api'] = True
            last_c = 'LoggingService'
        elif opt == '-D':
            options['directory_sync_api'] = True
            last_c = 'DirectorySyncService'
        elif opt == '-E':
            options['event_api'] = True
            last_c = 'EventService'
        elif opt == '--delete':
            options['delete'] = True
            last_m = 'delete'
        elif opt == '--poll':
            options['poll'] = True
            last_m = 'poll'
        elif opt == '--xpoll':
            options['xpoll'] = True
            last_m = 'xpoll'
        elif opt == '--query':
            options['query'] = True
            last_m = 'query'
        elif opt == '--write':
            options['write'] = True
            last_m = 'write'
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
            last_m = 'set_filters'
        elif opt == '--get':
            options['get'] = True
            last_m = 'get_filters'
        elif opt == '--ack':
            options['ack'] = True
            last_m = 'ack'
        elif opt == '--nack':
            options['nack'] = True
            last_m = 'nack'
        elif opt == '--follow':
            options['follow'] = True
        elif opt == '--count':
            options['count'] = True
            last_m = 'count'
        elif opt == '--domains':
            options['domains'] = True
            last_m = 'domains'
        elif opt == '--attributes':
            options['attributes'] = True
            last_m = 'attributes'
        elif opt in ['--R0', '--R1', '--R2']:
            _options_R(opt[2:], last_c, last_m, arg)
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
    if not options['credentials'] and 'ACCESS_TOKEN' in os.environ:
        headers = {
            'Authorization': 'Bearer %s' % os.environ['ACCESS_TOKEN'],
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    for k in list(options_R.keys()):
        init = None
        if k == 'R0' and headers is not None:
            init = {'headers': headers}
        options_R[k + '_obj'] = {}
        for x in options_R[k].keys():
            options_R[k + '_obj'][x] =\
                process_json_args(options_R[k][x], init)

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
    -C                    use Credentials() class
      --write             write_credentials() method
    --R0 json             class constructor args (**kwargs)
    --R1 json             class method body/QUERY_STRING (data/params)
    --R2 json             class method args (**kwargs)
                          multiple --R[012]'s allowed, will be merged
                          context/order dependent on previous class, method
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
