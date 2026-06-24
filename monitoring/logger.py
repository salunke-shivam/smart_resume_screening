import logging
import config

# create a logger for the app
logger = logging.getLogger("resume_screener")

# set level based on debug setting
if config.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# create a handler that prints to console
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# create a simple format
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

# add handler to logger
logger.addHandler(handler)


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)


def log_debug(message):
    logger.debug(message)


def log_warning(message):
    logger.warning(message)


def log_agent_action(agent_name, action, details=""):
    # log what an agent is doing
    msg = f"{agent_name} | {action}"
    if details:
        msg += f" | {details}"
    logger.info(msg)