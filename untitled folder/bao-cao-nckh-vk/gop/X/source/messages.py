"""The only accepted Gemini messages and their explicitly audited MP3 names."""
from pathlib import Path
from typing import Mapping

_pairs = (
 ("Đây là tờ năm trăm đồng.", "01-ay-la-to-nam-tram-ong.mp3"), ("Đây là tờ một ngàn đồng.", "02-ay-la-to-mot-ngan-ong.mp3"),
 ("Đây là tờ hai ngàn đồng.", "03-ay-la-to-hai-ngan-ong.mp3"), ("Đây là tờ năm ngàn đồng.", "04-ay-la-to-nam-ngan-ong.mp3"),
 ("Đây là tờ mười ngàn đồng.", "05-ay-la-to-muoi-ngan-ong.mp3"), ("Đây là tờ hai mươi ngàn đồng.", "06-ay-la-to-hai-muoi-ngan-ong.mp3"),
 ("Đây là tờ năm mươi ngàn đồng.", "07-ay-la-to-nam-muoi-ngan-ong.mp3"), ("Đây là tờ một trăm ngàn đồng.", "08-ay-la-to-mot-tram-ngan-ong.mp3"),
 ("Đây là tờ hai trăm ngàn đồng.", "09-ay-la-to-hai-tram-ngan-ong.mp3"), ("Đây là tờ năm trăm ngàn đồng.", "10-ay-la-to-nam-tram-ngan-ong.mp3"),
 ("Đây là cây bút.", "11-ay-la-cay-but.mp3"), ("Đây là cái chăn.", "12-ay-la-cai-chan.mp3"), ("Đây là chậu rửa.", "13-ay-la-chau-rua.mp3"),
 ("Đây là giẻ lau.", "14-ay-la-gie-lau.mp3"), ("Đây là đồng hồ.", "15-ay-la-ong-ho.mp3"), ("Đây là cái cốc.", "16-ay-la-cai-coc.mp3"),
 ("Đây là cái bát.", "17-ay-la-cai-bat.mp3"), ("Đây là cái ấm.", "18-ay-la-cai-am.mp3"), ("Đây là chìa khóa.", "19-ay-la-chia-khoa.mp3"),
 ("Đây là dao nhà bếp.", "20-ay-la-dao-nha-bep.mp3"), ("Đây là lá cây.", "21-ay-la-la-cay.mp3"), ("Đây là bóng đèn.", "22-ay-la-bong-en.mp3"),
 ("Đây là cái áo.", "23-ay-la-cai-ao.mp3"), ("Đây là lon kim loại.", "24-ay-la-lon-kim-loai.mp3"), ("Đây là quả cam hoặc quả quất.", "25-ay-la-qua-cam-hoac-qua-quat.mp3"),
 ("Đây là giấy.", "26-ay-la-giay.mp3"), ("Đây là túi nhựa.", "27-ay-la-tui-nhua.mp3"), ("Cảnh báo, đây là vật sắc nhọn nguy hiểm.", "28-canh-bao-ay-la-vat-sac-nhon-nguy-hiem.mp3"),
 ("Đây là cái thìa.", "29-ay-la-cai-thia.mp3"), ("Đây là cái thước.", "30-ay-la-cai-thuoc.mp3"), ("Đây là bàn chải đánh răng.", "31-ay-la-ban-chai-anh-rang.mp3"),
 ("Đây là chai nước.", "32-ay-la-chai-nuoc.mp3"), ("Đây là đôi đũa.", "33-ay-la-oi-ua.mp3"), ("Đây là rác vô cơ.", "34-ay-la-rac-vo-co.mp3"),
 ("Đây là rác hữu cơ.", "35-ay-la-rac-huu-co.mp3"), ("Đây là rác khác.", "36-ay-la-rac-khac.mp3"),
)
VALID_MESSAGES = tuple(message for message, _ in _pairs)
MESSAGE_TO_MP3: Mapping[str, str] = dict(_pairs)
FALLBACK_MESSAGE = VALID_MESSAGES[-1]

def normalize_and_validate(raw_text: str) -> str:
    text = raw_text.strip()
    return text if text in MESSAGE_TO_MP3 else FALLBACK_MESSAGE

def mp3_filename_for(message: str) -> str:
    return MESSAGE_TO_MP3.get(message, MESSAGE_TO_MP3[FALLBACK_MESSAGE])

def validate_message_catalog(mp3_dir: Path) -> None:
    if len(VALID_MESSAGES) != 36 or len(MESSAGE_TO_MP3) != 36 or len(set(MESSAGE_TO_MP3.values())) != 36:
        raise ValueError("Catalog thông báo không đủ/không một-một")
    missing = [name for name in MESSAGE_TO_MP3.values() if not (mp3_dir / name).is_file()]
    if missing:
        raise FileNotFoundError("Thiếu MP3: " + ", ".join(missing))
