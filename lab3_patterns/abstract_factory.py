from __future__ import annotations
from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...


class WindowsButton(Button):
    def render(self) -> str:
        return "Render Windows button"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "Render Windows checkbox"


class MacButton(Button):
    def render(self) -> str:
        return "Render Mac button"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "Render Mac checkbox"


class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


def build_ui(factory: GUIFactory) -> list[str]:
    return [factory.create_button().render(), factory.create_checkbox().render()]
