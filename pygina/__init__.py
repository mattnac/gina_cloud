from typing import List
from pydantic import BaseModel
import regex as re
import gtts
from pygame import mixer
from playsound import playsound
from io import BytesIO
import datetime
import inflection
from xml.etree.ElementTree import Element

from typing import Callable, Any
import sys, logging
import PySimpleGUI as sg
from overlay import Window
mixer.init()


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

    name: str = None
    trigger_text: str = None
    comments: str = None
    enable_regex: bool = None
    use_text: bool = None
    display_text: str = None
    copy_to_clipboard: bool = None
    clipboard_text: str = None
    use_text_to_voice: bool = None
    interrupt_speech: bool = None
    text_to_voice_text: str = None
    play_media_file: bool = None
    timer_type: str  = None # Make enum
    timer_name: str = None
    restart_based_on_timer_name: bool = None
    timer_millisecond_duration: int = None
    timer_duration: int = None
    timer_visible_duration: int = None
    timer_start_behaviour: str = None # Make enum
    timer_ending_time: int = None
    user_timer_ending: bool = None
    user_timer_ended: bool = None
    use_counter_reset_timer: bool = None
    counter_reset_duration: int = None
    category: str = None
    modified: str = None # change to datetime and create a setter
    use_fast_check: bool = None
    timer_early_enders: str = None # not sure about what type this is
    reg_ex: re.Pattern = None


    @property
    def trigger_regex(self) -> re:
        if self.reg_ex is None:
            self.reg_ex = re.compile(self.trigger_text.replace("?<", "?P<"))
        return self.reg_ex

    def match(self, line: str) -> bool:
        #line = re.sub('\[.*\]', '', line)
        result = self.trigger_regex.search(line)

        if result:
            groups = dict()

            for k,v in self.trigger_regex.search(line).groupdict().items():
                groups[k.lower()] = v.strip()
            if self.text_to_voice_text is not None:

                mp3_fp = BytesIO()
                speech = self.text_to_voice_text.lower().format(**groups).replace("$","")

                tts = gtts.gTTS(speech, lang='en', slow=False)
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                mixer.music.load(mp3_fp)
                mixer.music.play()
            # TODO: FIGURE OUT OVERLAY
            # if self.timer_duration > 0:
            #     layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400),
            #                         background_color='red', enable_events=True, key='graph')],
            #               [sg.Text('Change circle color to:'), sg.Button('Red'), sg.Button('Blue'), sg.Button('Move')]]
            #
            #     window = sg.Window('Graph test', layout, finalize=True)
            #
            #     graph = window['graph']  # type: sg.Graph
            #     circle = graph.draw_circle((75, 75), 25, fill_color='black', line_color='white')
            #     point = graph.draw_point((75, 75), 10, color='green')
            #     oval = graph.draw_oval((25, 300), (100, 280), fill_color='purple', line_color='purple')
            #     rectangle = graph.draw_rectangle((25, 300), (100, 280), line_color='purple')
            #     line = graph.draw_line((0, 0), (100, 100))
            #     arc = graph.draw_arc((0, 0), (400, 400), 160, 10, style='arc', arc_color='blue')
            #     poly = graph.draw_polygon(((10, 10), (20, 0), (40, 200), (10, 10)), fill_color='green')
            #     while True:
            #         event, values = window.read()
            #         print(event, values)
            #         if event == sg.WIN_CLOSED:
            #             break
            #         if event in ('Blue', 'Red'):
            #             graph.TKCanvas.itemconfig(circle, fill=event)
            #         elif event == 'Move':
            #             graph.MoveFigure(point, 10, 10)
            #             graph.MoveFigure(circle, 10, 10)
            #             graph.MoveFigure(oval, 10, 10)
            #             graph.MoveFigure(rectangle, 10, 10)
            #             graph.MoveFigure(arc, 10, 10)
            #             graph.MoveFigure(poly, 10, 10)
        return result
    # def __init__(self, xml: Element):
    #
    #     for node in xml.findall("./"):
    #         self.__dict__[inflection.underscore(node.tag)] = node.text



TriggerList = list()
