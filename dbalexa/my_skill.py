from ask_sdk_core.skill_builder import SkillBuilder,CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler,AbstractResponseInterceptor,AbstractRequestInterceptor,AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type,is_intent_name
from ask_sdk_core.attributes_manager import AbstractPersistenceAdapter,AttributesManager
from ask_sdk_core.exceptions import AttributesManagerException

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, StopDirective)
from copy import deepcopy
from .alexa import data
from .alexa import util

sb = CustomSkillBuilder()


from dbalexa.models import AudioData
from django.http import HttpResponse

import requests
# class MyAbstractPersistenceAdapter(AbstractPersistenceAdapter):
#     def get_attributes(self, request_envelope):
#         # type: (RequestEnvelope) -> Dict[str, object]
#         """Get attributes from persistent tier.

#         :param request_envelope: Request Envelope from Alexa service
#         :type request_envelope: RequestEnvelope
#         :return: A dictionary of attributes retrieved from persistent
#             tier
#         :rtype: Dict[str, object]
#         """
#         pass

#     def save_attributes(self, request_envelope, attributes):
#         # type: (RequestEnvelope, Dict[str, object]) -> None
#         """Save attributes to persistent tier.

#         :param request_envelope: request envelope.
#         :type request_envelope: RequestEnvelope
#         :param attributes: attributes to be saved to persistent tier
#         :type attributes: Dict[str, object]
#         :rtype: None
#         """
#         pass

   
#     def delete_attributes(self, request_envelope):
#         # type: (RequestEnvelope) -> None
#         """Delete attributes from  persistent tier.

#         :param request_envelope: request envelope.
#         :type request_envelope: RequestEnvelope
#         :rtype: None
#         """
#         pass
# class MyAttributesManager(AttributesManager):
#     """AttributesManager is a class that handles three level
#     attributes: request, session and persistence.

#     :param request_envelope: request envelope.
#     :type request_envelope: RequestEnvelope
#     :param persistence_adapter: class used for storing and
#         retrieving persistent attributes from persistence tier
#     :type persistence_adapter: AbstractPersistenceAdapter
#     """

#     def __init__(self, request_envelope, persistence_adapter=None):
#         # type: (RequestEnvelope, AbstractPersistenceAdapter) -> None
#         """AttributesManager handling three level of
#         attributes: request, session and persistence.

#         :param request_envelope: request envelope.
#         :type request_envelope: RequestEnvelope
#         :param persistence_adapter: class used for storing and
#             retrieving persistent attributes from persistence tier
#         :type persistence_adapter: AbstractPersistenceAdapter
#         """
#         if request_envelope is None:
#             raise AttributesManagerException("RequestEnvelope cannot be none!")
#         self._request_envelope = request_envelope
#         self._persistence_adapter = persistence_adapter
#         self._persistence_attributes = {}  # type: Dict
#         self._request_attributes = {}  # type: Dict
#         if request_envelope.session is None:
#             self._session_attributes = None  # type: Optional[Dict[str, Any]]
#         elif request_envelope.session.attributes is None:
#             self._session_attributes = {}
#         else:
#             self._session_attributes = deepcopy(
#                 request_envelope.session.attributes)
#         self._persistent_attributes_set = False

#     @property
#     def request_attributes(self):
#         # type: () -> Dict[str, object]
#         """Attributes stored at the Request level of the skill lifecycle.

#         :return: request attributes for the request life cycle
#         :rtype: Dict[str, object]
#         """
#         return self._request_attributes

#     @request_attributes.setter
#     def request_attributes(self, request_attributes):
#         # type: (Dict[str, object]) -> None
#         """

#         :param request_attributes: attributes for the request life cycle
#         :type request_attributes: Dict[str, object]
#         """
#         self._request_attributes = request_attributes

#     @property
#     def session_attributes(self):
#         # type: () -> Optional[Dict[str, Any]]
#         """Attributes stored at the Session level of the skill lifecycle.

#         :return: session attributes extracted from request envelope
#         :rtype: Dict[str, object]
#         """
#         if not self._request_envelope.session:
#             raise AttributesManagerException(
#                 "Cannot get SessionAttributes from out of session request!")
#         return self._session_attributes

#     @session_attributes.setter
#     def session_attributes(self, session_attributes):
#         # type: (Dict[str, object]) -> None
#         """

#         :param session_attributes: attributes during the session
#         :type session_attributes: Dict[str, object]
#         :raises: :py:class:`ask_sdk_core.exceptions.AttributesManagerException`
#             if trying to set session attributes to out of session request
#         """
#         if not self._request_envelope.session:
#             raise AttributesManagerException(
#                 "Cannot set SessionAttributes to out of session request!")
#         self._session_attributes = session_attributes

#     @property
#     def persistent_attributes(self):
#         # type: () -> Dict[str, object]
#         """Attributes stored at the Persistence level of the skill lifecycle.

#         :return: persistent_attributes retrieved from persistence adapter
#         :rtype: Dict[str, object]
#         :raises: :py:class:`ask_sdk_core.exceptions.AttributesManagerException`
#             if trying to get persistent attributes without persistence adapter
#         """
#         if not self._persistence_adapter:
#             raise AttributesManagerException(
#                 "Cannot get PersistentAttributes without Persistence adapter")
#         if not self._persistent_attributes_set:
#             self._persistence_attributes = (
#                 self._persistence_adapter.get_attributes(
#                     request_envelope=self._request_envelope))
#             self._persistent_attributes_set = True
#         return self._persistence_attributes

#     @persistent_attributes.setter
#     def persistent_attributes(self, persistent_attributes):
#         # type: (Dict[str, object]) -> None
#         """Overwrites and caches the persistent attributes value.

#         Note that the persistent attributes will not be saved to
#         persistence layer until the save_persistent_attributes method
#         is called.

#         :param persistent_attributes: attributes in persistence layer
#         :type persistent_attributes: Dict[str, object]
#         :raises: :py:class:`ask_sdk_core.exceptions.AttributesManagerException`
#             if trying to set persistent attributes without persistence adapter
#         """
#         if not self._persistence_adapter:
#             raise AttributesManagerException(
#                 "Cannot set PersistentAttributes without persistence adapter!")
#         self._persistence_attributes = persistent_attributes
#         self._persistent_attributes_set = True

#     def save_persistent_attributes(self):
#         # type: () -> None
#         """Save persistent attributes to the persistence layer if a
#         persistence adapter is provided.

#         :rtype: None
#         :raises: :py:class:`ask_sdk_core.exceptions.AttributesManagerException`
#             if trying to save persistence attributes without persistence adapter
#         """
#         if not self._persistence_adapter:
#             raise AttributesManagerException(
#                 "Cannot save PersistentAttributes without "
#                 "persistence adapter!")
#         if self._persistent_attributes_set:
#             self._persistence_adapter.save_attributes(
#                 request_envelope=self._request_envelope,
#                 attributes=self._persistence_attributes)

#     def delete_persistent_attributes(self):
#         # type: () -> None
#         """Deletes the persistent attributes from the persistence layer.

#         :rtype: None
#         :raises: :py:class: `ask_sdk_core.exceptions.AttributesManagerException`
#             if trying to delete persistence attributes without persistence adapter
#         """
#         if not self._persistence_adapter:
#             raise AttributesManagerException(
#                 "Cannot delete PersistentAttributes without "
#                 "persistence adapter!")

#         self._persistence_adapter.delete_attributes(
#             request_envelope=self._request_envelope)
#         self._persistence_attributes = {}
#         self._persistent_attributes_set = False


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
             WELCOME_PLAYBACK_MSG ="Welcome back to Gita Hexa. It’s good to see you again. You were listening to adhyay "+ audio_data.index +". Would you like to resume? You can say yes to resume or no to play from the top"  
             message = WELCOME_PLAYBACK_MSG
             reprompt=data.WELCOME_PLAYBACK_REPROMPT_MSG 
        handler_input.response_builder.speak(message).ask(reprompt)
        
        
        print(handler_input.response_builder.response)
        
        return handler_input.response_builder.speak(message).ask(reprompt).response
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
        
        return (in_playback_session
                and (is_intent_name("AMAZON.StopIntent")(handler_input)
                     or is_intent_name("AMAZON.CancelIntent")(handler_input)
                     or is_intent_name("AMAZON.PauseIntent")(handler_input)))


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
        
        return (not in_playback_session
                and (is_intent_name("AMAZON.CancelIntent")(handler_input)
                     or is_intent_name("AMAZON.StopIntent")(handler_input)))

    def handle(self, handler_input):
        # offset_info_data=get_offset(handler_input)
        # user_id=get_user_info(handler_input)
        # audio_data=AudioData.objects.get(user_id=user_id)
        # audio_data.offset_in_milliseconds=offset_info_data
        # audio_data.has_previous_playback_session=True
        # audio_data.in_playback_session=False
        # audio_data.save()
        # print("===========CancelOrStopIntentHandler handle==============")
        # # response_builder = handler_input.response_builder
        # # response_builder.speak(data.STOP_MSG)
        
        return handler_input.response_builder.speak(data.STOP_MSG).response

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
        
        return handler_input.response_builder.speak(message).ask(message).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        print("=============session ended==============")
        return handler_input.response_builder.response
class PlaybackStartedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStarted Directive received.
    Confirming that the requested audio file began playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("=============In PlaybackStartedHandler can_handle============")
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("=============In PlaybackStartedHandler handle============")

        # playback_info = util.get_playback_info(handler_input)
        # playback_info["token"] = util.get_token(handler_input)
        # playback_info["index"] = util.get_index(handler_input)
        # playback_info["in_playback_session"] = True
        # playback_info["has_previous_playback_session"] = True

        return handler_input.response_builder.response
class PlaybackFinishedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFinished Directive received.
    Confirming that the requested audio file completed playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("===========PlaybackFinishedEventHandler can_handle=============")
        return is_request_type("AudioPlayer.PlaybackFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("===========PlaybackFinishedEventHandler handle=============")

        return handler_input.response_builder.response
class PlaybackStoppedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStopped Directive received.
    Confirming that the requested audio file stopped playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("===========PlaybackStoppedEventHandler can_handle=============")
        return is_request_type("AudioPlayer.PlaybackStopped")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("===========PlaybackStoppedEventHandler handle=============")
        return handler_input.response_builder.response

class PlaybackNearlyFinishedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackNearlyFinished Directive received.
    Replacing queue with the URL again. This should not happen on live streams.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("===========PlaybackNearlyFinishedEventHandler can_handle=============")
        return is_request_type("AudioPlayer.PlaybackNearlyFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("===========PlaybackNearlyFinishedEventHandler handle=============")
        return handler_input.response_builder.response
class PlaybackFailedEventHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFailed Directive received.
    Logging the error and restarting playing with no output speech.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("===========PlaybackFailedEventHandler can_handle=============")
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("===========PlaybackFailedEventHandler handle=============")

        return handler_input.response_builder.response
class ExceptionEncounteredHandler(AbstractRequestHandler):
    """Handler to handle exceptions from responses sent by AudioPlayer
    request.
    """
    def can_handle(self, handler_input):
        # type; (HandlerInput) -> bool
        print("===========ExceptionEncounteredHandler can_handle=============")
        return is_request_type("System.ExceptionEncountered")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("===========ExceptionEncounteredHandler handle=============")
        print("===========Exception=============")
        print(handler_input.request_envelope.request)
        return handler_input.response_builder.response
class LoadPersistenceAttributesRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("hellooo form AbstractRequestInterceptor")
sb.skill_id = "amzn1.ask.skill.745a6bcb-042c-4177-ab28-c50a3c0317ef"
# sb.persistence_adapter=MyAbstractPersistenceAdapter



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
sb.add_request_handler(PlaybackFinishedEventHandler())
sb.add_request_handler(PlaybackStoppedEventHandler())
sb.add_request_handler(PlaybackFailedEventHandler())
sb.add_request_handler(PlaybackNearlyFinishedEventHandler())
sb.add_request_handler(ExceptionEncounteredHandler())
# sb.add_request_handler(PersistenceAttributesHandler())

sb.add_global_request_interceptor(LoadPersistenceAttributesRequestInterceptor())
# sb.add_global_response_interceptor(SavePersistenceAttributesResponseInterceptor())
# sb.add_request_handler(FallbackIntentHandler())

# sb.add_request_handler(ExceptionEncounteredHandler())
# sb.add_exception_handler(CatchAllExceptionHandler())



skill = sb.create()

