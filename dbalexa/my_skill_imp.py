from ask_sdk_core.skill_builder import SkillBuilder,CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler,AbstractResponseInterceptor,AbstractRequestInterceptor,AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type,is_intent_name
from ask_sdk_core.attributes_manager import AbstractPersistenceAdapter,AttributesManager
from .alexa import data
from .alexa import util
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, StopDirective)
sb = CustomSkillBuilder()
sb.skill_id = "amzn1.ask.skill.745a6bcb-042c-4177-ab28-c50a3c0317ef"
from dbalexa.models import AudioData
from django.http import HttpResponse
from ask_sdk_model import Response
from django.shortcuts import render
import requests
def main(request):
    return render(request,'index.html')
def get_user_info(handler_input):
    user_info =handler_input.request_envelope.context.system.user.user_id
    return user_info
def get_offset(handler_input):
    offset_info=handler_input.request_envelope.context.audio_player.offset_in_milliseconds
    return offset_info

def play(handler_input):
    user_id=get_user_info(handler_input)
    audio_data=AudioData.objects.get(user_id=user_id)
    audio_data.in_playback_session=True
    audio_data.has_previous_playback_session=True
    audio_data.save()
    play_index=int(audio_data.index)
    url=data.AUDIO_DATA[play_index]["url"]
    offset_info_data=audio_data.offset_in_milliseconds
    message="playing adhyay "+ audio_data.index + "from bhagvad gita hexa"
    response_builder = handler_input.response_builder.speak(message)
    response_builder.add_directive(
        PlayDirective(
            play_behavior="REPLACE_ALL",
            audio_item=AudioItem(
                stream=Stream(
                    token="A",
                    url=url,
                    offset_in_milliseconds=offset_info_data,
                    expected_previous_token=None),
                    metadata=None))
    ).set_should_end_session(True)
    print(handler_input.response_builder.response)
    return response_builder.response


class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        print(handler_input.request_envelope)
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        user_id=get_user_info(handler_input)
        try:
            audio_data = AudioData.objects.get(pk=user_id)
        except AudioData.DoesNotExist:
            audio_data = audio_data=AudioData(user_id,0,1,0,0,0)
            audio_data.save()
        has_previous_playback_session=audio_data.has_previous_playback_session
        print(audio_data.has_previous_playback_session)
        if not has_previous_playback_session:
            message = data.WELCOME_MSG
            reprompt = data.WELCOME_REPROMPT_MSG
        else:
             audio_data = AudioData.objects.get(pk=user_id)
             WELCOME_PLAYBACK_MSG = "You were listening to adhyay "+ audio_data.index +". Would you like to resume?"  
             message = WELCOME_PLAYBACK_MSG
             reprompt=data.WELCOME_PLAYBACK_REPROMPT_MSG 
        message = data.WELCOME_MSG
        reprompt = data.WELCOME_REPROMPT_MSG
        handler_input.response_builder.speak(message).ask(reprompt)
        print(handler_input.response_builder.response)
        return handler_input.response_builder.response
    


class StartPlaybackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("IntentRequest")(handler_input) and is_intent_name("PlayAudio")(handler_input) )

    def handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        play_index=handler_input.request_envelope.request.intent.slots['adhyaynumber'].value
        audio_data.offset_in_milliseconds=0
        audio_data.index=play_index
        audio_data.save()
        return play(handler_input)
class PlaybackStartedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStarted Directive received.
    Confirming that the requested audio file began playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("=============In PlaybackStartedHandler============")

        # playback_info = util.get_playback_info(handler_input)

        # playback_info["token"] = util.get_token(handler_input)
        # playback_info["index"] = util.get_index(handler_input)
        # playback_info["in_playback_session"] = True
        # playback_info["has_previous_playback_session"] = True

        return handler_input.response_builder.response
class StartPlaybackResumeHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        in_playback_session=audio_data.in_playback_session
        return (in_playback_session and is_intent_name("AMAZON.ResumeIntent")(handler_input))

    def handle(self, handler_input):
        return play(handler_input)


class PausePlaybackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        in_playback_session=audio_data.in_playback_session
        print("===========PausePlaybackHandler can handle==============")
        return (in_playback_session and is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        offset_info_data=get_offset(handler_input)
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        audio_data.offset_in_milliseconds=offset_info_data
        audio_data.save()
        response_builder = handler_input.response_builder
        response_builder.add_directive(StopDirective())
        print("===========PausePlaybackHandler  handle==============")
        return response_builder.response
class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        print("===========CancelOrStopIntentHandler can handle==============")
        in_playback_session=audio_data.in_playback_session
        return ( in_playback_session and (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
        is_intent_name("AMAZON.StopIntent")(handler_input)))

    def handle(self, handler_input):
        offset_info_data=get_offset(handler_input)
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        audio_data.offset_in_milliseconds=offset_info_data
        audio_data.has_previous_playback_session=True
        audio_data.in_playback_session=False
        audio_data.save()
        print("===========CancelOrStopIntentHandler handle==============")
        response_builder = handler_input.response_builder
        response_builder.speak(data.STOP_MSG)
        response_builder.add_directive(StopDirective()).set_should_end_session(True)
        return response_builder.response

class NextPlaybackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("IntentRequest")(handler_input) and is_intent_name("AMAZON.NextIntent")(handler_input))
    
    def handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        play_index=int(audio_data.index)+1
        audio_data.offset_in_milliseconds=0
        audio_data.index=play_index
        audio_data.save()
        return play(handler_input)

class YesHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        in_playback_session=audio_data.in_playback_session
        return (not in_playback_session and is_intent_name("AMAZON.YesIntent")(handler_input))

    def handle(self, handler_input):
        return play(handler_input)
class NoHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        in_playback_session=audio_data.in_playback_session
        return (not in_playback_session and is_intent_name("AMAZON.NoIntent")(handler_input))

    def handle(self, handler_input):
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        audio_data.index=1
        audio_data.offset_in_milliseconds=0
        audio_data.save()        
        return play(handler_input)
class HelpIntentHandler(AbstractRequestHandler):
 
    def can_handle(self, handler_input):
       
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        user_id=get_user_info(handler_input)
        try:
            audio_data = AudioData.objects.get(pk=user_id)
        except AudioData.DoesNotExist:
            audio_data = audio_data=AudioData(user_id,0,1,0,0,0)
            audio_data.save()
        has_previous_playback_session=audio_data.has_previous_playback_session
        in_playback_session=audio_data.in_playback_session
        if not has_previous_playback_session:
            message = data.HELP_MSG
        elif not in_playback_session:
            message = data.HELP_PLAYBACK_MSG
        else:
            message = data.HELP_DURING_PLAY_MSG
        message = data.HELP_MSG
        return handler_input.response_builder.speak(message).ask(message).response
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak(data.EXCEPTION_MSG)
        return handler_input.response_builder.response
class SessionEndedRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class PlaybackStoppedEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackStopped")(handler_input)

    def handle(self, handler_input):
        offset_info_data=get_offset(handler_input)
        user_id=get_user_info(handler_input)
        audio_data=AudioData.objects.get(user_id=user_id)
        audio_data.offset_in_milliseconds=offset_info_data
        audio_data.has_previous_playback_session=True
        audio_data.in_playback_session=False
        audio_data.save()
        return handler_input.response_builder.response
class ExceptionEncounteredHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("System.ExceptionEncountered")(handler_input)
    
    def handle(self, handler_input):
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        print(handler_input.request_envelope.context.audio_player.offset_in_milliseconds)
        return True

    def handle(self, handler_input, exception):
        return handler_input.response_builder.response




sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartPlaybackHandler())
sb.add_request_handler(PausePlaybackHandler())
sb.add_request_handler(StartPlaybackResumeHandler())
sb.add_request_handler(NextPlaybackHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(PlaybackStartedEventHandler())
# sb.add_request_handler(FallbackIntentHandler())

# sb.add_request_handler(ExceptionEncounteredHandler())
# sb.add_exception_handler(CatchAllExceptionHandler())



skill = sb.create()

