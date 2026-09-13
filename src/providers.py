"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return (
            "Smart Job Application Agent giúp bạn theo dõi hồ sơ ứng tuyển, "
            "cập nhật trạng thái Kanban và đặt lịch phỏng vấn. "
            "Các thao tác trên dữ liệu cụ thể cần được thực hiện qua Agent có Tools."
        )

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        if "giới thiệu" in prompt_lower or "cách trợ lý" in prompt_lower:
            return {
                "type": "text",
                "content": "Smart Job Application Agent theo dõi hồ sơ ứng tuyển, cập nhật trạng thái Kanban và hỗ trợ đặt lịch phỏng vấn.",
                "thought": "Đây là câu hỏi giới thiệu chung, không cần gọi Tool."
            }
        if "observation từ tool search_job_status" in prompt_lower:
            if '"status": "not_found"' in prompt_lower:
                return {
                    "type": "text",
                    "content": "Không tìm thấy hồ sơ ứng tuyển phù hợp nên tôi chưa thực hiện cập nhật hoặc đặt lịch.",
                    "thought": "Hồ sơ không tồn tại, dừng luồng để tránh bịa đặt dữ liệu."
                }
            if "chuyển" in prompt_lower or "interviewing" in prompt_lower:
                return {
                    "type": "tool_call",
                    "tool_name": "update_application_kanban",
                    "arguments": {"job_id": "JOB-VINGROUP-001", "status": "Interviewing"},
                    "thought": "Hồ sơ đã được tìm thấy, cập nhật trạng thái sang Interviewing."
                }
            return {
                "type": "text",
                "content": "Hồ sơ Vingroup là vị trí Data Analyst, trạng thái hiện tại là To Apply.",
                "thought": "Đã nhận kết quả tra cứu và có thể trả lời trực tiếp."
            }
        if "observation từ tool update_application_kanban" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "schedule_interview_calendar",
                "arguments": {
                    "title": "Phỏng vấn Data Analyst - Vingroup",
                    "time": "2026-09-18T14:00:00"
                },
                "thought": "Hồ sơ đã chuyển sang Interviewing, tiếp tục đặt lịch phỏng vấn."
            }
        if "observation từ tool schedule_interview_calendar" in prompt_lower:
            if "xử lý hồ sơ" in prompt_lower:
                content = "Đã cập nhật hồ sơ sang Interviewing và đặt lịch phỏng vấn Data Analyst tại Vingroup vào 14:00 ngày 18/09/2026."
            else:
                content = "Đã đặt lịch phỏng vấn Data Analyst tại Vingroup vào 14:00 ngày 18/09/2026."
            return {
                "type": "text",
                "content": content,
                "thought": "Chuỗi xử lý ứng tuyển đã hoàn tất."
            }
        if "không tồn tại" in prompt_lower:
            company = "Không Tồn Tại"
        else:
            company = "Vingroup"
        if "tra cứu" in prompt_lower or "trạng thái" in prompt_lower or "xử lý hồ sơ" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "search_job_status",
                "arguments": {"company": company, "student_id": "2A202602835"},
                "thought": f"Tra cứu hồ sơ ứng tuyển tại {company} trước khi thực hiện bước tiếp theo."
            }
        if "đặt lịch" in prompt_lower or "phỏng vấn" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "schedule_interview_calendar",
                "arguments": {"title": "Phỏng vấn Data Analyst - Vingroup", "time": "2026-09-18T14:00:00"},
                "thought": "Người dùng yêu cầu đặt lịch phỏng vấn với thời gian cụ thể."
            }
        return {
            "type": "text",
            "content": "Smart Job Application Agent theo dõi hồ sơ, cập nhật Kanban và hỗ trợ đặt lịch phỏng vấn.",
            "thought": "Câu hỏi chung có thể trả lời trực tiếp."
        }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
