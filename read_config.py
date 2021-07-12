from custom_logging import get_logger
import yaml

logger = get_logger(__name__, only_debug=True)

with open('config.yml', 'r') as f:
    stream = f.read()
config = yaml.safe_load(stream)
logger.debug("Parsed config.yml")

def get_reply(msg: str, **kwargs) -> str:
    """ Replace placeholders in the reply template with actual values. """

    reply = config['MESSAGES'][msg]
    if kwargs:
        for var_count in range(reply.count('{')):
            placeholder = reply[reply.find('{') : reply.find('}')+1]
            var_name = placeholder[1:len(placeholder)-1]
            reply = reply.replace(placeholder, kwargs[var_name])

    logger.debug("Built a reply.")
    return reply