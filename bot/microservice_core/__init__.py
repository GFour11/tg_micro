import os
import sys
import io
import importlib

if '--force-color' in sys.argv:
    sys.stdout.isatty = lambda: True

for k in os.environ:
    if k.upper() == 'D':
        try:
            port = int(os.environ[k])
        except ValueError:
            port = int(os.environ.get("DEBUG_PORT", 5678))
        sys.path.append('/lib/pydevd-pycharm.egg')

        # import pydevd_pycharm
        pydevd_pycharm = importlib.import_module('pydevd_pycharm')
        from .lib import print_red, boolean_input

        original_stderr = sys.stderr
        sys.stderr = captured_stderr = io.StringIO()

        host = os.environ.get("DEBUG_HOST", 'host.docker.internal')

        try:
            pydevd_pycharm.settrace(host, port=port, suspend=False)
        except ConnectionRefusedError:
            # captured_stderr.getvalue() contains the error
            print_red(
                f"Warning! Script is running in debug mode, but no debugger is listening on {host}:{port}"
            )
            if not boolean_input("Do you want to continue?", default=False):
                exit(0)
        finally:
            sys.stderr = original_stderr
