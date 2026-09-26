"""Button input using Raspberry Pi's recommended gpiozero library."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ButtonController:
    button: object
    gpio_number: int


def setup_button(gpio_number: int, debounce_seconds: float) -> ButtonController:
    """Configure BCM GPIO input with an internal pull-up.

    gpiozero uses the system pin factory; with lgpio installed this is the
    recommended backend on current 64-bit DietPi versions for Pi Zero 2 W.
    """
    try:
        from gpiozero import Button
    except ImportError as exc:
        raise RuntimeError(
            "Thiếu gpiozero/lgpio; cài bằng apt hoặc pip trên Raspberry Pi"
        ) from exc

    button = Button(
        gpio_number,
        pull_up=True,
        bounce_time=debounce_seconds,
    )
    return ButtonController(button=button, gpio_number=gpio_number)


def wait_for_press(controller: ButtonController) -> None:
    controller.button.wait_for_press()


def wait_for_release(controller: ButtonController) -> None:
    controller.button.wait_for_release()


def close_button(controller: Optional[ButtonController]) -> None:
    if controller is not None:
        controller.button.close()
