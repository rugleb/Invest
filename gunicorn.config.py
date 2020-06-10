from multiprocessing import cpu_count
from os import getenv as env

from invest_api import log, settings

STDOUT = "-"

# The number of pending connections.
backlog = env("GUNICORN_BACKLOG", 2048)

# The socket to bind.
bind = env("GUNICORN_BIND", f"0.0.0.0:{settings.PORT}")

# Check the configuration.
check_config = env("GUNICORN_CHECK_CONFIG", False)

# The number of worker processes that this server
# should keep alive for handling requests.
workers = env("GUNICORN_WORKERS", cpu_count() * 2 + 1)

# The type of workers to use.
worker_class = env("GUNICORN_WORKER_CLASS", "aiohttp.GunicornUVLoopWebWorker")

# The maximum number of requests a worker will process before restarting.
# Any value greater than zero will limit the number of requests
# a work will process before automatically restarting.
max_requests = env("GUNICORN_MAX_REQUESTS", 100)

# If a worker does not notify the master process in this number of
# seconds it is killed and a new worker is spawned to replace it.
timeout = env("GUNICORN_TIMEOUT", 10)

# Timeout for graceful workers restart.
graceful_timeout = env("GUNICORN_GRACEFUL_TIMEOUT", 5)

# The number of seconds to wait for the next
# request on a Keep-Alive HTTP connection.
keepalive = env("GUNICORN_KEEPALIVE", 5)

# Install a trace function that spews every line of Python
# that is executed when running the server.
# This is the nuclear option.
spew = env("GUNICORN_SPEW", False)

# Detach the main Gunicorn process from the controlling
# terminal with a standard fork sequence.
daemon = env("GUNICORN_DAEMON", False)

# The path to a log file to write to.
logfile = env("GUNICORN_LOGFILE", STDOUT)

# The granularity of log output.
loglevel = env("GUNICORN_LOGLEVEL", log.LEVEL)

# The Error log file to write to.
errorlog = env("GUNICORN_ERRORLOG", STDOUT)

# The Access log file to write to.
accesslog = env("GUNICORN_ACCESSLOG", STDOUT)

# The access log format.
access_log_format = log.ACCESS_LOG_FORMAT

# The log config dictionary to use, using the standard Python
# logging module’s dictionary configuration format.
logconfig_dict = log.CONFIG

# A base to use with setproctitle for process naming
proc_name = env("GUNICORN_PROC_NAME", "invest_api")

# Internal setting that is adjusted for each type of application.
default_proc_name = env("GUNiCORN_DEFAULT_PROC_NAME", "invest_api")
