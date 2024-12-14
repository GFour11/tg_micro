from typing import Union

import inspect
import sys
import traceback
import logging
import os
import subprocess
from termcolor import colored
from typing import Callable
from decimal import Decimal
from datetime import datetime, timezone
from decimal import getcontext, ROUND_DOWN


# noinspection SpellCheckingInspection
def set_decimal_context(prec=18, rounding=ROUND_DOWN):
    context = getcontext()
    context.prec = prec
    context.rounding = rounding


def percent_to_float(s: str):
    if s == "" or s is None:
        return 0
    s = str(s).replace(',', '.')
    _s = s
    s = str(float(str(s).rstrip("%")))
    i = s.find(".")
    if s.startswith("-"):
        return -percent_to_float(_s.lstrip("-"))
    s = s.replace(".", "")
    if _s[-1] == '%':
        i -= 2
    if i < 0:
        return float("." + "0" * abs(i) + s)
    else:
        return float(s[:i] + "." + s[i:])


def is_percent(s: str):
    return s.endswith('%')


def get_constants_values(class_object):
    constants = []
    for attr in dir(class_object):
        if attr.isupper():
            constants.append(getattr(class_object, attr))
    return constants


def catch_and_log_exceptions(exit_after: bool = False, callback_after: Callable = None, logger: str = ''):
    def __wrapper_func(_func):
        def _wrapper(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return _func(*args, **kwargs)
            except BaseException:
                output = traceback.format_exc().split("\n")
                logging.getLogger(logger).error("\n".join(output[0:1]+output[3:]))
                # print("\n".join(output[0:1]+output[3:]), file=sys.stderr)
                # sys.stderr.flush()
            if callback_after is not None and callable(callback_after):
                callback_after()
            if exit_after:
                sys.exit(1)

        return _wrapper

    return __wrapper_func


def non_critical(get_logger_name: Callable, arg: Union[int, str] = 0, app: str = 'application'):
    """
    Decorator for catching exceptions and logging them without exit.
    Parameters
    ----------
    :param get_logger_name: Callable
    :param arg: int | str = 0 (default: 0) - index of argument in function args or kwargs
    :param app: str (default: application) - name of application

    Returns
    -------


    """
    def _non_critical(func):
        def wrapper(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return func(*args, **kwargs)
            except BaseException:
                output = traceback.format_exc().split("\n")
                method_args = inspect.getfullargspec(func).args
                if type(arg) is int:
                    assert arg < len(method_args), "arg index is out of range"
                    arg_value = args[arg]
                else:
                    if arg in kwargs:
                        arg_value = kwargs[arg]
                    else:
                        assert arg in method_args, "arg name is not in method args"
                        arg_value = args[method_args.index(arg)]

                logger = app + '.' + get_logger_name(arg_value) + '.non_critical'
                logging.getLogger(logger).error("\n".join(output[0:1]+output[3:]))
        return wrapper
    return _non_critical


def seconds_to_hms_str(seconds: int, seconds_round: int = 2) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{int(hours)}h:{int(minutes)}m:{round(seconds, seconds_round)}s'


def has_float_part(decimal_number: Decimal):
    return decimal_number.as_tuple().exponent < 0


def normalize_decimal_number_to_str(number: Decimal) -> str:
    if number <= 1e-4:
        return "{:.8f}".format(number).rstrip("0").rstrip(".")
    else:
        result = Decimal("{:.8f}".format(number)).normalize()
        if not has_float_part(result):
            result = int(result)
        return str(result)


def parse_dt(dt) -> Union[datetime, None]:
    if dt is None:
        return None
    try:
        return datetime.strptime(dt, "%Y-%m-%d_%H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def get_minutes_passed_by_day(dt: datetime) -> int:
    date_hours = dt.hour
    date_minutes = dt.minute
    return date_hours * 60 + date_minutes


def timestamp_to_milliseconds(timestamp: Union[float, None] = None) -> int:
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    return int(timestamp * 1000)


def run_subprocess(args, save_lines_count=4, drop_output: bool = False):
    print("> ", ' '.join(args))

    env = os.environ.copy()
    if 'D' in env:
        del env['D']

    if drop_output:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL
    else:
        stdout = subprocess.PIPE
        stderr = None

    process = subprocess.Popen(args, stdout=stdout, stderr=stderr, text=True, env=env)
    output = []

    if not drop_output:
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            if save_lines_count > 0:
                output.append(line)
                if len(output) > save_lines_count:
                    del output[0]
        process.communicate()
        process.stdout.close()
    process.wait()

    return output


def boolean_input(question, default=None):
    if default is None:
        question = "%s [y/n] " % question
    elif default is True:
        question = "%s [Y/n] " % question
    elif default is False:
        question = "%s [y/N] " % question
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    result = None
    try:
        result = input("%s " % question)
    except KeyboardInterrupt:
        print('')
        exit(0)

    if not result and default is not None:
        return default
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes or no: ")
    return result[0].lower() == "y"


def check_is_containers_logs_disabled():
    if 'C_LOGS' not in os.environ or os.environ['C_LOGS'] != '0':
        print("Must be run with C_LOGS=0 (C_LOGS=0 python file.py ...")
        exit(1)


def print_red(text):
    print(colored(text, 'red'))


def print_green(text):
    print(colored(text, 'green'))