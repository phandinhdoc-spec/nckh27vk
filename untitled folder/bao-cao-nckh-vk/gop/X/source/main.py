import logging
from dataclasses import dataclass
from config import AppConfig, load_config, BUTTON_GPIO_BCM
from messages import normalize_and_validate, mp3_filename_for, validate_message_catalog
from camera import capture_jpeg, delete_file_if_exists
from gemini_client import classify
from audio import play_mp3, play_fallback, resolve_mp3_path
from button import setup_button, wait_for_press, wait_for_release, close_button

@dataclass
class Services: button: object
def process_one_press(config, services):
    image_path = None
    try:
        image_path = capture_jpeg(config)
        message = normalize_and_validate(classify(image_path, config))
        play_mp3(resolve_mp3_path(config.mp3_dir, mp3_filename_for(message)), config)
    except Exception as exc:
        logging.getLogger(__name__).exception("Lỗi xử lý lượt nhấn: %s", exc)
        try: play_fallback(config)
        except Exception: logging.getLogger(__name__).exception("Không phát được fallback")
    finally: delete_file_if_exists(image_path)
def run():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = load_config(); validate_message_catalog(config.mp3_dir)
    controller = setup_button(BUTTON_GPIO_BCM, config.debounce_seconds)
    try:
        while True:
            wait_for_press(controller); process_one_press(config, Services(controller)); wait_for_release(controller)
    except KeyboardInterrupt: pass
    finally: close_button(controller)
if __name__ == "__main__": run()
