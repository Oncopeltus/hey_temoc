
intent_lst = ["purple", "orange", "gold", "green", "red", "grey"]
intent_dict = {
    "purple": {"parking structure 1": "5", "parking structure 3": "10", "parking structure 10": "6"},
    "orange": {"parking structure 1": "6", "parking structure 3": "11", "parking structure 10": "7"},
    "gold": {"parking structure 1": "7", "parking structure 3": "12", "parking structure 10": "5"},
    "green": {"parking structure 1": "3", "parking structure 3": "6", "parking structure 10": "1"},
    "red": {"parking structure 1": "5", "parking structure 3": "10", "parking structure 10": "6"},
    "grey": {"parking structure 1": "5", "parking structure 3": "10", "parking structure 10": "6"}
}

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

#------------------------------Part3--------------------------------
# Here we define the Request handler functions

def on_start():
    print("Session Started.")

def on_launch(event):
    onlaunch_MSG = "Hi, what color parking permit do you have?"
    reprompt_MSG = "Do you have purple, orange, gold, or green permit? or you want to use pay spots?"
    card_TEXT = "Pick a topic."
    card_TITLE = "Choose a topic."
    return output_json_builder_with_reprompt_and_card(onlaunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")

#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request.
# Since we have a few different intents in our skill, we need to
# configure what this function will do upon receiving a particular
# intent. This can be done by introducing the functions which handle
# each of the intents.

def intent_scheme(event):
    intent_name = event['request']['intent']['name']
    if intent_name in intent_lst:
        return intenthandler(event, intent_name)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
    else:
        return errorhandler(event)

#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions
def intenthandler(event, intent_name):
    '''
    if ("resolutions" not in event['request']['intent']['slots'][intent_name + 'Item']):
        MSG = "What do you want to know about it? You can choose among these terms: " + ', '.join(intent_dict[intent_name].keys()) + "."
        reprompt_MSG = "Do you want to hear more about the " + intent_name + "?"
        card_TEXT = "Need more detail."
        card_TITLE = "Truncated name."
        return output_json_builder_with_reprompt_and_card(MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    if event['request']['intent']['slots'][intent_name + 'Item']['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == "ER_SUCCESS_MATCH":

        name = event['request']['intent']['slots'][intent_name + 'Item']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        reprompt_MSG = "Do you want to hear more about the bookstore?"
        card_TEXT = "you've picked " + name.lower()
        card_TITLE = "you've picked " + name.lower()
        output = intent_dict[intent_name][1]
        return output_json_builder_with_reprompt_and_card(output, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
    '''
        num1 = str(intent_dict[intent_name]["parking structure 1"])
        num3 = str(intent_dict[intent_name]["parking structure 3"])
        num4 = str(intent_dict[intent_name]["parking structure 4"])

        MSG = "There are " + num1 + "spots available in parking structure 1, and " + num3 + "spots available in parking structure 3, and "+ num4 + "spots available in parking structure 4 for your permit."
        reprompt_MSG = "Do you want to hear the number of spots available for " + intent_name + " permit?"
        card_TEXT = "you've picked " + intent_name.lower()
        card_TITLE = "you've picked " + intent_name.lower()
        return output_json_builder_with_reprompt_and_card(output, card_TEXT, card_TITLE, reprompt_MSG, False)
def errorhandler(event):
        wrongname_MSG = "Sorry I do not understand. You can choose among these terms: " + ', '.join(intent_dict[intent_name].keys()) + "."
        reprompt_MSG = "Do you want to hear more about the " + intent_name + "parking?"
        card_TEXT = "Use the correct option."
        card_TITLE = "Wrong input."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)


def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)

def assistance(event):
    assistance_MSG = "You can choose among these terms: " + ', '.join(map(str, BookStore_OBJ_lst)) + ". Be sure to use the exact phrases."
    reprompt_MSG = "Do you want to hear more?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format.
# That is why in this part of the code we define the functions which
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to
# build the output.

def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict

def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
