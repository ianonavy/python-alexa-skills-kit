"""Utility functions for building responses for Alexa Skills Kit."""

from collections import namedtuple


AlexaResponse = namedtuple('AlexaResponse', [
    'session_attributes',
    'output_speech',
    'card_title',
    'reprompt_text',
    'should_end_session'
])


def plain_text_speech_to_dict(output_speech):
    return {
        'type': "PlainText",
        'text': output_speech
    }


def response_to_dict(alexa_response):
    """Converts an `AlexaResponse` into a nested dictionary.

    Supports the format from Alexa Skills Kit version 1.0.

    :param alexa_response: An `AlexaResponse` object
    :return: Dictionary formatted according to the Alexa Skills Kit
    """
    output_speech = plain_text_speech_to_dict(alexa_response.output_speech)
    reprompt_text = plain_text_speech_to_dict(alexa_response.reprompt_text)
    return {
        'version': "1.0",
        'sessionAttributes': alexa_response.session_attributes,
        'response': {
            'outputSpeech': output_speech,
            'card': {
                'type': "Simple",
                'title': "SessionSpeechlet - " + alexa_response.card_title,
                'content': alexa_response.output_speech
            },
            'reprompt': reprompt_text,
            'shouldEndSession': alexa_response.should_end_session
        }
    }
