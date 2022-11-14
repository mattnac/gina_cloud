from typing import List
from pydantic import BaseModel
import re
import datetime
import inflection
from xml.etree.ElementTree import Element


class BaseClass(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class Trigger(BaseClass):
    """
      <Name>sieve</Name>
      <TriggerText>^(?&lt;mob&gt;.*) staggers in pain\.$</TriggerText>
      <Comments />
      <EnableRegex>True</EnableRegex>
      <UseText>True</UseText>
      <DisplayText>Sieve on ${mob}</DisplayText>
      <CopyToClipboard>True</CopyToClipboard>
      <ClipboardText>/gu  [ ${mob}  ]  has been sieved {COUNTER} times</ClipboardText>
      <UseTextToVoice>True</UseTextToVoice>
      <InterruptSpeech>True</InterruptSpeech>
      <TextToVoiceText>${mob} sievied  {COUNTER} times</TextToVoiceText>
      <PlayMediaFile>False</PlayMediaFile>
      <TimerType>Timer</TimerType>
      <TimerName>sieve ${mob}</TimerName>
      <RestartBasedOnTimerName>False</RestartBasedOnTimerName>
      <TimerMillisecondDuration>60000</TimerMillisecondDuration>
      <TimerDuration>60</TimerDuration>
      <TimerVisibleDuration>0</TimerVisibleDuration>
      <TimerStartBehavior>RestartTimer</TimerStartBehavior>
      <TimerEndingTime>1</TimerEndingTime>
      <UseTimerEnding>False</UseTimerEnding>
      <UseTimerEnded>False</UseTimerEnded>
      <UseCounterResetTimer>False</UseCounterResetTimer>
      <CounterResetDuration>0</CounterResetDuration>
      <Category>Default</Category>
      <Modified>2022-11-13T17:33:33</Modified>
      <UseFastCheck>True</UseFastCheck>
      <TimerEarlyEnders />
    """

    name: str
    trigger_text: str
    comments: str
    enable_regex: bool
    use_text: bool
    display_text: str
    copy_to_clipboard: bool
    clipboard_text: str
    use_text_to_voice: bool
    interrupt_speech: bool
    text_to_voice_text: str
    play_media_file: bool
    timer_type: str  # Make enum
    timer_name: str
    restart_based_on_timer_name: bool
    timer_millisecond_duration: int
    timer_duration: int
    timer_visible_duration: int
    timer_start_behaviour: str  # Make enum
    timer_ending_time: int
    user_timer_ending: bool
    user_timer_ended: bool
    use_counter_reset_timer: bool
    counter_reset_duration: int
    category: str
    modified: str  # change to datetime and create a setter
    use_fast_check: bool
    timer_early_enders: str  # not sure about what type this is

    _reg_ex: re = None

    @property
    def trigger_regex(self) -> re:
        if self._reg_ex is None:
            self._reg_ex = re.compile(self.trigger_text.replace("?<", "?P<"))
        return self._reg_ex

    def __init__(self, xml: Element):

        for node in xml.findall("./"):
            self.__dict__[inflection.underscore(node.tag)] = node.text


TriggerList = List[Trigger]
