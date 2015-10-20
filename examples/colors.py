"""Sample AWS Lambda function for remembering a favorite color."""

from alexa import AlexaSkill, AlexaResponse, intent_callback


class Color(AlexaSkill):

    card_title = "Favorite Color"

    def _get_welcome(self):
        reprompt_text = ("Please tell me your favorite color by saying, "
                         "my favorite color is red")
        output_speech = ("Welcome to the Alexa Skills Kit sample, " +
                         reprompt_text)
        return AlexaResponse(session_attributes={},
                             output_speech=output_speech,
                             card_title=self.card_title,
                             reprompt_text=reprompt_text,
                             should_end_session=False)

    def handle_launch(self, request, session):
        return self._get_welcome()

    @intent_callback('HelpIntent')
    def on_help(self, intent, session):
        return self._get_welcome()

    @intent_callback('MyColorIsIntent')
    def on_my_color_is(self, intent, session):
        slot = intent['slots'].get("Color")
        print(slot)
        if slot:
            favorite_color = slot['value']
            output_speech = ("I now know your favorite color is {}. You can "
                             "ask me your favorite color by saying, what's "
                             "my favorite color?".format(favorite_color))
            reprompt_text = ("You can ask me your favorite color by saying, "
                             "what's my favorite color?")
            session_attributes = {'favoriteColor': favorite_color}
        else:
            output_speech = ("I'm not sure what your favorite color is, "
                             "please try again")
            reprompt_text = ("I'm not sure what your favorite color is, "
                             "you can tell me your favorite color by saying, "
                             "my favorite color is red")
            session_attributes = {}
        return AlexaResponse(session_attributes=session_attributes,
                             output_speech=output_speech,
                             card_title=self.card_title,
                             reprompt_text=reprompt_text,
                             should_end_session=False)

    @intent_callback('WhatsMyColorIntent')
    def on_whats_my_color(self, intent, session):
        favorite_color = session.get("favoriteColor")
        if favorite_color:
            output_speech = ("Your favorite color is {}, Ian".format(
                favorite_color))
            should_end_session = True
        else:
            output_speech = ("I'm not sure what your favorite color is. "
                             "You can say, my favorite color is red")
            should_end_session = False
        return AlexaResponse(session_attributes={},
                             output_speech=output_speech,
                             card_title=self.card_title,
                             reprompt_text=None,
                             should_end_session=should_end_session)


def lambda_handler(event, context):
    return Color().handle(event, context)


if __name__ == '__main__':
    import json
    event = {
        'request': {
            'type': "IntentRequest",
            'intent': {
                'slots': {
                    "Color": 'red'
                },
                'name': "MyColorIsIntent",
                'requestId': "request5678"
            }
        },
        'session': {
            'new': False
        },
        'version': "1.0"
    }
    context = None
    print(json.dumps(lambda_handler(event, context), indent=2))
