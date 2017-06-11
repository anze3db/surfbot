"""lambda_function.py main entry point for aws lambda"""

import json
import urllib.request
from typing import Dict, Optional

import settings
from logger import logger


def close(fulfillment_state: str, message: Dict[str, str]) -> dict:
    """Close dialog generator"""
    return {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }


def lambda_handler(event: dict, _: dict) -> Optional[dict]:
    """Lambda Handler
       Entry point for every lambda function call
    """
    if not settings.MSW_API:
        logger.error("Couldn't read SF_MSW_API env variable")
        return None

    logger.debug('event.bot.name=%s', event['bot']['name'])
    logger.debug('dispatch userId=%s, intentName=%s', event['userId'],
                 event['currentIntent']['name'])

    res = json.loads(urllib.request.urlopen(
        "http://magicseaweed.com/api/{}/forecast/?spot_id=912".format(
            settings.MSW_API)).read())
    logger.debug('json.response=%s', res)

    return close('Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'This worked! {}'.format(res[0]['solidRating'])})
