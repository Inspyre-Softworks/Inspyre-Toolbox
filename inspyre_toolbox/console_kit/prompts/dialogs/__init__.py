from prompt_toolkit import ANSI, HTML
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog

from inspyre_toolbox.console_kit.prompts import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.log_engine import Loggable, ROOT_LOGGER
from inspyre_toolbox.syntactic_sweets.locks import flag_lock
from inspyre_toolbox.syntactic_sweets.classes.decorators import validate_type

ROOT_LOGGER.set_level(console_level='DEBUG')
MOD_LOGGER = PARENT_LOGGER.get_child('dialogs')


class ConfirmationPrompt(Loggable):
    DIALOG_TITLE_STUB = 'Please Confirm '
    DIALOG_TEXT_STUB = 'Are you sure you want to '
    DIALOG_TEXT_SUFFIX = '?'
    DIALOG_BASE = yes_no_dialog

    def __init__(self, title: str, text: str, no_title_stub=False, no_text_stub=False, no_text_suffix=False):

        super().__init__(MOD_LOGGER)

        self.__burnt = False
        self._burning = None
        self.__title = None
        self.__text = None

        self.__no_title_stub = None
        self.__no_text_stub = None

        self.no_title_stub = no_title_stub
        self.no_text_stub = no_text_stub

        title = title.title()

        if not self.no_title_stub:
            self.title = f'{self.DIALOG_TITLE_STUB}{title}'
        else:
            self.title = title

        text = f'{text.capitalize()}{"" if no_text_suffix else self.DIALOG_TEXT_SUFFIX}'

        self.text = text if self.no_text_stub else f'{self.DIALOG_TEXT_STUB}{text}'

    @property
    def answer(self) -> bool:
        return self.__answer if self.burnt else None

    @answer.setter
    @validate_type(bool)
    def answer(self, new: bool):
        if self.burning:
            self.__answer = new
            return

        if not self.burnt:
            raise AttributeError('This prompt has not been presented yet.')
        else:
            raise AttributeError('This property can only be set while the prompt is running and has not been run yet.')

    @property
    def burning(self):
        return self._burning

    @burning.setter
    @validate_type(bool)
    def burning(self, new: bool):
        self._burning = new

    @property
    def burnt(self) -> bool:
        return self.__burnt

    @burnt.setter
    @validate_type(bool)
    def burnt(self, new: bool):
        self.check_burnt()
        self.__burnt = new

    @property
    def no_text_stub(self) -> bool:
        return self.__no_text_stub

    @no_text_stub.setter
    @validate_type(bool)
    def no_text_stub(self, new: bool):
        self.check_burnt()
        self.__no_text_stub = new

    @property
    def no_title_stub(self) -> bool:
        return self.__no_title_stub

    @no_title_stub.setter
    @validate_type(bool)
    def no_title_stub(self, new: bool):
        self.check_burnt()
        self.__no_title_stub = new

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    @validate_type(str)
    def title(self, new: str):
        self.check_burnt()
        self.__title = new

    @property
    def text(self) -> str:
        self.check_burnt()
        return self.__text

    @text.setter
    @validate_type(str)
    def text(self, new: str):
        self.check_burnt()
        self.__text = new

    def check_burnt(self):
        if self.burnt and not self.burning:
            raise AttributeError('This prompt has already been burnt.')

    def run(self) -> bool:
        log = self.create_logger()
        log.debug(f'Running confirmation prompt: {self.title} with text {self.text}')
        if self.burning:
            raise RuntimeError('This prompt is already running.')

        # Log the type of self.text
        log.debug(f'Type of self.text: {type(self.text)}')

        # Ensure self.text is of the correct type
        if not isinstance(self.text, (str, HTML, ANSI)):
            raise ValueError(f'Invalid text type: {type(self.text)}. Expected str, HTML, ANSI, or FormattedText.')

        self.burnt = True
        with flag_lock(self, 'burning'):
            self.answer = yes_no_dialog(title=self.title, text=self.text).run()

            return self.answer
