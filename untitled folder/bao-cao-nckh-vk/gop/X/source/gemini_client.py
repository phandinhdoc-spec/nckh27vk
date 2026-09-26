import base64, json, logging, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from config import AppConfig, build_gemini_endpoint
from messages import VALID_MESSAGES

PROMPT = """Bạn là bộ phân loại hình ảnh cho thiết bị hỗ trợ người khiếm thị.
Chỉ được trả về đúng một câu duy nhất, khớp chính xác một câu trong danh sách. Không JSON, Markdown, giải thích hay dấu ngoặc kép. Nếu ảnh mờ, không chắc, nhiều vật ngang nhau hoặc không thuộc nhóm rõ ràng, trả về: Đây là rác khác.
Ưu tiên tiền giấy Việt Nam đọc rõ mệnh giá, sau đó vật sắc nhọn nguy hiểm, vật thể cụ thể; nếu không thì rác hữu cơ/vô cơ/khác. Không suy đoán từ tên file hay lịch sử. Nhận diện: bút, chăn/mền, chậu rửa, giẻ lau, đồng hồ, cốc/ly, bát, ấm, chìa khóa, dao nhà bếp, lá cây, bóng đèn, áo, lon kim loại, cam/quất, giấy, túi nhựa, vật sắc nhọn nguy hiểm, thìa, thước, bàn chải đánh răng, chai nước, đũa. Tiền được phép: 500, 1.000, 2.000, 5.000, 10.000, 20.000, 50.000, 100.000, 200.000, 500.000 đồng.
DANH SÁCH HỢP LỆ (sao chép đúng từng ký tự):
""" + "\n".join(VALID_MESSAGES) + "\nBây giờ hãy xem ảnh và trả về đúng một câu trong danh sách trên."

def build_prompt() -> str: return PROMPT
def build_payload(prompt, image_base64, config):
    return {"contents":[{"parts":[{"text":prompt},{"inline_data":{"mime_type":"image/jpeg","data":image_base64}}]}],"generationConfig":{"temperature":0,"candidateCount":1,"maxOutputTokens":40}}
def extract_response_text(response):
    try: return response["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc: raise ValueError("Gemini response thiếu text hoặc bị chặn") from exc
def classify(image_path: Path, config: AppConfig) -> str:
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    body = json.dumps(build_payload(build_prompt(), encoded, config)).encode()
    for attempt in range(config.retry_count + 1):
        try:
            req = Request(build_gemini_endpoint(config), data=body, headers={"Content-Type":"application/json"}, method="POST")
            with urlopen(req, timeout=config.http_timeout) as response: return extract_response_text(json.load(response))
        except HTTPError as exc:
            if exc.code < 500 or attempt >= config.retry_count: raise RuntimeError(f"Gemini HTTP {exc.code}") from exc
        except (URLError, TimeoutError, OSError) as exc:
            if attempt >= config.retry_count: raise RuntimeError("Gemini network error") from exc
        time.sleep(0.2)
