"""Alexa Skills represent the logic used to build JSON responses to
events as specified in the Alexa Skills Kit."""

import functools

from alexa.response import response_to_dict


def intent_callback(intent_name):
    """Makes the decorated method activate on the correct intent.

    This crazy black magic works by doing a runtime check on the name
    of the intent and returning None if it doesn't match. This means
    that every registered function is called.

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, intent, session):
            if intent['name'] == intent_name:
                return func(self, intent, session)
            else:
                return None
        return wrapper
    return decorator


class AlexaSkill(object):
    """Base class for an Alexa Skill."""

    def __init__(self):
        self._intents = {}

    def handle(self, event, context):
        """Main entry point into the Alexa Skill.

        Most Alexa Skills should not need to override this method.

        :param event: The AWS Lambda event
        :param context: The AWS Lambda context
        :return: The response built
        """
        request = event['request']
        session = event['session']
        response = None

        print(request)
        print(session)

        if session['new']:
            self.start_session(request['requestId'], session)

        request_type = request['type']
        if request_type == 'LaunchRequest':
            alexa_response = self.handle_launch(request, session)
            response = response_to_dict(alexa_response)
        elif request_type == 'IntentRequest':
            alexa_response = self.handle_intent(request['intent'], session)
            response = response_to_dict(alexa_response)
        elif request_type == 'SessionEndedRequest':
            self.end_session(request, session)

        print(response)

        return response

    def start_session(self, request, session):
        """Handles a new Amazon Echo session.

        This method should be used to initialize any state needed for
        a session. The return value is not used.

        :param request: The request object from the Amazon Echo event
        :param session: The session object from the Amazon Echo event
        """
        pass

    def handle_launch(self, request, session):
        """Handles a LaunchRequest from the Amazon Echo.

        :param request: The request object from the Amazon Echo event
        :param session: The session object from the Amazon Echo event
        :return: Session attributes and speechlet response
        """
        raise NotImplementedError("Must override handle_launch")

    def handle_intent(self, intent, session):
        """Handles an intent from the Amazon Echo.

        Most Alexa Skills should not need to override this method.
        Instead, subclasses should define methods and use the
        `intent_callback` decorator to associate their methods with
        a particular intent.

        Note: this is horrible black magic and can probably be dealt
        with in a cleaner fashion, but it makes the API really pretty,
        so I've decided to keep it.

        :param intent: The intent object from the Amazon Echo request
        :param session: The session object from the Amazon Echo event
        :return: Session attributes and speechlet response
        """
        # Get the first public method defined in the subclass *not*
        # defined in this superclass that does not return None
        subclass_methods = set(dir(self)) - set(dir(AlexaSkill()))
        ret = None
        for subclass_method in subclass_methods:
            if not subclass_method.startswith('_'):
                method = getattr(self, subclass_method)
                if hasattr(method, '__call__'):
                    ret = method(intent, session)
                    if ret is not None:
                        break
        return ret

    def end_session(self, request, session):
        """Handles the end of an Amazon Echo session.

        The return value is not used.

        :param intent: The intent object from the Amazon Echo request
        :param session: The session object from the Amazon Echo event
        """
        pass
