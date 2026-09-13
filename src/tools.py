"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "search_job_status",
        "description": "Tra cứu trạng thái hồ sơ ứng tuyển của sinh viên theo công ty.",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "Tên công ty cần tra cứu"
                },
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu"
                }
            },
            "required": ["company", "student_id"]
        }
    },
    {
        "name": "update_application_kanban",
        "description": "Cập nhật trạng thái hồ sơ ứng tuyển trên Kanban.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "Mã hồ sơ ứng tuyển"
                },
                "status": {
                    "type": "string",
                    "description": "Trạng thái mới của hồ sơ, ví dụ 'Interviewing'"
                }
            },
            "required": ["job_id", "status"]
        }
    },
    {
        "name": "schedule_interview_calendar",
        "description": "Đặt lịch phỏng vấn trên lịch cá nhân.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Tiêu đề cuộc phỏng vấn"
                },
                "time": {
                    "type": "string",
                    "description": "Thời gian phỏng vấn theo ISO 8601"
                }
            },
            "required": ["title", "time"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

JOB_APPLICATIONS = {
    ("VINGROUP", "2A202602835"): {
        "job_id": "JOB-VINGROUP-001",
        "role": "Data Analyst",
        "current_status": "To Apply"
    }
}


def execute_search_job_status(company: str, student_id: str) -> str:
    """Tra cứu hồ sơ ứng tuyển theo công ty và mã sinh viên."""
    application = JOB_APPLICATIONS.get((company.strip().upper(), student_id.strip().upper()))
    if application:
        return json.dumps({
            "status": "SUCCESS",
            "data": application
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy hồ sơ ứng tuyển của sinh viên {student_id} tại công ty {company}."
    }, ensure_ascii=False)


def execute_update_application_kanban(job_id: str, status: str) -> str:
    """Cập nhật trạng thái hồ sơ ứng tuyển."""
    for application in JOB_APPLICATIONS.values():
        if application["job_id"] == job_id:
            application["current_status"] = status
            return json.dumps({
                "status": "SUCCESS",
                "message": f"Job status updated to '{status}'"
            }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy hồ sơ có mã '{job_id}'."
    }, ensure_ascii=False)


def execute_schedule_interview_calendar(title: str, time: str) -> str:
    """Tạo lịch phỏng vấn trên lịch cá nhân."""
    return json.dumps({
        "status": "SUCCESS",
        "event_link": "https://calendar.google.com/calendar/event?eid=mock_link",
        "title": title,
        "time": time
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "search_job_status": execute_search_job_status,
    "update_application_kanban": execute_update_application_kanban,
    "schedule_interview_calendar": execute_schedule_interview_calendar
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)


if __name__ == "__main__":
    required_tools = {
        "search_job_status",
        "update_application_kanban",
        "schedule_interview_calendar"
    }
    registered_tools = {tool["name"] for tool in TOOLS_SCHEMA}
    if required_tools.issubset(registered_tools):
        print("✅ [TOOLS CHECK]: Đã đăng ký thành công 3 Native Tools tuyển dụng!")

    result = json.loads(dispatch_tool_call(
        "search_job_status",
        {"company": "Vingroup", "student_id": "2A202602835"}
    ))
    print(
        f"🧪 Kết quả gọi thử search_job_status: Status {result.get('status')} "
        f"(Job ID {result.get('data', {}).get('job_id', 'N/A')})"
    )
