from __future__ import annotations

import base64
import json
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class MacClientError(RuntimeError):
    pass


class ServerError(MacClientError):
    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.status = status
        self.code = code
        self.message = message


class MacClient:
    def __init__(self, server_url: str, token: str, timeout: int, retries: int) -> None:
        self.server_url = server_url
        self.token = token
        self.timeout = timeout
        self.retries = retries

    def plan(self, text: str) -> dict[str, object]:
        """Ask Mac whether a command needs a camera image before capturing."""
        clean_text = text.strip()
        if not clean_text:
            raise MacClientError("Nội dung lệnh đang trống.")
        data = json.dumps({"text": clean_text}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        body, content_type, _ = self._post("/plan", data, "application/json", 64 * 1024)
        if not content_type.startswith("application/json"):
            raise MacClientError("Mac trả sai Content-Type cho /plan.")
        try:
            result = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise MacClientError("Mac trả JSON kế hoạch không hợp lệ.") from error
        if (
            not isinstance(result, dict)
            or not isinstance(result.get("command"), str)
            or result.get("mode") not in {"local", "auto", "chat", "ocr", "observe"}
            or not isinstance(result.get("needsImage"), bool)
        ):
            raise MacClientError("Mac trả kế hoạch thiếu command, mode hoặc needsImage.")
        return result

    def command(
        self,
        text: str,
        image: bytes | None = None,
        mode: str | None = None,
        sensor: dict[str, object] | None = None,
    ) -> tuple[bytes, str]:
        payload: dict[str, object] = {"text": text}
        if mode is not None:
            payload["mode"] = mode
        if sensor:
            payload["sensor"] = sensor
        if image is not None:
            payload["image"] = base64.b64encode(image).decode("ascii")
            payload["imageContentType"] = "image/jpeg"
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        body, content_type, encoded_text = self._post(
            "/command", data, "application/json", 10 * 1024 * 1024
        )
        if not content_type.startswith("audio/mpeg"):
            raise MacClientError("Mac trả sai Content-Type cho /command.")
        if not body:
            raise MacClientError("Mac trả file MP3 rỗng.")
        try:
            answer_text = (
                base64.b64decode(encoded_text, validate=True).decode("utf-8")
                if encoded_text
                else ""
            )
        except (ValueError, UnicodeDecodeError) as error:
            raise MacClientError("Mac trả header text Gemini không hợp lệ.") from error
        return body, answer_text

    def _post(
        self,
        path: str,
        data: bytes,
        content_type: str,
        response_limit: int,
    ) -> tuple[bytes, str, str | None]:
        request = Request(
            self.server_url + path,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": content_type,
            },
        )
        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    body = response.read(response_limit + 1)
                    if len(body) > response_limit:
                        raise MacClientError("Phản hồi từ Mac vượt quá giới hạn cho phép.")
                    return (
                        body,
                        response.headers.get_content_type().lower(),
                        response.headers.get("X-ThienNhan-Text-Base64"),
                    )
            except HTTPError as error:
                raise _server_error(error) from error
            except (URLError, TimeoutError, socket.timeout) as error:
                if attempt >= self.retries:
                    raise MacClientError(f"Không thể kết nối Mac: {error}") from error
                time.sleep(min(2**attempt, 3))
        raise AssertionError("Vòng retry kết thúc ngoài dự kiến.")


def _server_error(error: HTTPError) -> ServerError:
    raw = error.read(64 * 1024)
    code = "server_error"
    message = error.reason or "Mac xử lý thất bại."
    try:
        payload = json.loads(raw)
        detail = payload.get("error", {})
        if isinstance(detail, dict):
            code = str(detail.get("code") or code)
            message = str(detail.get("message") or message)
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
        pass
    return ServerError(error.code, code, message)
