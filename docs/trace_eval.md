# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Văn Thăng  
> **Mã Sinh Viên / Mã Học viên:** 2A202602835  
> **Chủ đề Lựa chọn:** Trợ lý Quản lý Tiến độ Ứng tuyển & Lên lịch Phỏng vấn (Smart Job Application Agent)  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4 / 5** | Agent cần thực hiện chuỗi hành động suy luận nối tiếp: Bóc tách thực thể (tên công ty, thời gian) -> tra cứu ID vị trí ứng tuyển -> cập nhật trạng thái Kanban -> đặt lịch Calendar. |
| **2. Tool Interaction** | **5 / 5** | Hệ thống bắt buộc phải kết nối với ít nhất 2 API bên ngoài: Cơ sở dữ liệu ứng tuyển (Notion/Trello/SQL) và Ứng dụng lịch trình (Google Calendar/Outlook API). |
| **3. Dynamic Decision** | **4 / 5** | Hành động tiếp theo phụ thuộc vào kết quả của tool trước. VD: Nếu `search_job_status` không tìm thấy công ty, Agent sẽ dừng luồng đặt lịch, chuyển sang hỏi người dùng hoặc tự động gọi tool `create_new_job_application`. |
| **4. Long Horizon Goal** | **4 / 5** | Hệ thống duy trì mục tiêu dài hạn là hỗ trợ sinh viên vượt qua kỳ phỏng vấn. Sau khi lên lịch, Agent ghi nhớ bối cảnh để tiếp tục đề xuất tạo bộ câu hỏi Mock Interview từ JD đã lưu. |
| **TỔNG ĐIỂM AGENTIC FIT** | **17 / 20** | *Kết luận: Đạt 17/20 điểm (> 12/20). Đề tài giải quyết bài toán thực tế của sinh viên, độ phức tạp logic cao, cực kỳ phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG

> ⚠️ **YÊU CẦU NGHIỆM THU API THẬT:** Khi nghiệm thu chính thức, mở tệp `.env` điền `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` trước khi chạy `python src/app.py --all`. Trace bên dưới mô tả workflow chuẩn của TC04.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Chào bạn, bạn có thể giới thiệu cách trợ lý quản lý tiến độ ứng tuyển và lên lịch phỏng vấn hoạt động không?",
    "action_type": "FINAL_ANSWER",
    "thought": "Đây là câu hỏi giới thiệu chung, không cần gọi Tool.",
    "output": "Smart Job Application Agent theo dõi hồ sơ ứng tuyển, cập nhật trạng thái Kanban và hỗ trợ đặt lịch phỏng vấn.",
    "latency_ms": 1357.44
  },
  {
    "step": 1,
    "query": "Hãy tra cứu trạng thái hồ sơ ứng tuyển của tôi tại công ty Vingroup.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_job_status",
    "arguments": {
      "company": "Vingroup",
      "student_id": "2A202602835"
    },
    "observation": {
      "status": "SUCCESS",
      "data": {
        "job_id": "JOB-VINGROUP-001",
        "role": "Data Analyst",
        "current_status": "To Apply"
      }
    },
    "latency_ms": 1171.16
  },
  {
    "step": 2,
    "query": "Hãy tra cứu trạng thái hồ sơ ứng tuyển của tôi tại công ty Vingroup.\n\nObservation từ tool search_job_status: {\"status\": \"SUCCESS\", \"data\": {\"job_id\": \"JOB-VINGROUP-001\", \"role\": \"Data Analyst\", \"current_status\": \"To Apply\"}}\nHãy tiếp tục suy luận. Nếu đã đủ dữ liệu, trả lời bằng văn bản trực tiếp.",
    "action_type": "FINAL_ANSWER",
    "thought": "Đã nhận kết quả tra cứu và có thể trả lời trực tiếp.",
    "output": "Hồ sơ Vingroup là vị trí Data Analyst, trạng thái hiện tại là To Apply.",
    "latency_ms": 957.21
  },
  {
    "step": 1,
    "query": "Hãy đặt lịch phỏng vấn vị trí Data Analyst tại Vingroup vào lúc 14:00 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_interview_calendar",
    "arguments": {
      "title": "Phỏng vấn Data Analyst - Vingroup",
      "time": "2026-09-18T14:00:00"
    },
    "observation": {
      "status": "SUCCESS",
      "event_link": "https://calendar.google.com/calendar/event?eid=mock_link",
      "title": "Phỏng vấn Data Analyst - Vingroup",
      "time": "2026-09-18T14:00:00"
    },
    "latency_ms": 795.77
  },
  {
    "step": 2,
    "query": "Hãy đặt lịch phỏng vấn vị trí Data Analyst tại Vingroup vào lúc 14:00 ngày 18/09/2026.\n\nObservation từ tool schedule_interview_calendar: {\"status\": \"SUCCESS\", \"event_link\": \"https://calendar.google.com/calendar/event?eid=mock_link\", \"title\": \"Phỏng vấn Data Analyst - Vingroup\", \"time\": \"2026-09-18T14:00:00\"}\nHãy tiếp tục suy luận. Nếu đã đủ dữ liệu, trả lời bằng văn bản trực tiếp.",
    "action_type": "FINAL_ANSWER",
    "thought": "Chuỗi xử lý ứng tuyển đã hoàn tất.",
    "output": "Đã đặt lịch phỏng vấn Data Analyst tại Vingroup vào 14:00 ngày 18/09/2026.",
    "latency_ms": 917.09
  },
  {
    "step": 1,
    "query": "Hãy xử lý hồ sơ ứng tuyển Data Analyst của tôi tại Vingroup: tra cứu trạng thái, chuyển hồ sơ sang Interviewing nếu phù hợp, rồi đặt lịch phỏng vấn lúc 14:00 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_job_status",
    "arguments": {
      "company": "Vingroup",
      "student_id": "2A202602835"
    },
    "observation": {
      "status": "SUCCESS",
      "data": {
        "job_id": "JOB-VINGROUP-001",
        "role": "Data Analyst",
        "current_status": "To Apply"
      }
    },
    "latency_ms": 944.42
  },
  {
    "step": 2,
    "query": "Hãy xử lý hồ sơ ứng tuyển Data Analyst của tôi tại Vingroup: tra cứu trạng thái, chuyển hồ sơ sang Interviewing nếu phù hợp, rồi đặt lịch phỏng vấn lúc 14:00 ngày 18/09/2026.\n\nObservation từ tool search_job_status: {\"status\": \"SUCCESS\", \"data\": {\"job_id\": \"JOB-VINGROUP-001\", \"role\": \"Data Analyst\", \"current_status\": \"To Apply\"}}\nHãy tiếp tục suy luận. Nếu đã đủ dữ liệu, trả lời bằng văn bản trực tiếp.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "update_application_kanban",
    "arguments": {
      "job_id": "JOB-VINGROUP-001",
      "status": "Interviewing"
    },
    "observation": {
      "status": "SUCCESS",
      "message": "Job status updated to 'Interviewing'"
    },
    "latency_ms": 811.89
  },
  {
    "step": 3,
    "query": "Hãy xử lý hồ sơ ứng tuyển Data Analyst của tôi tại Vingroup: tra cứu trạng thái, chuyển hồ sơ sang Interviewing nếu phù hợp, rồi đặt lịch phỏng vấn lúc 14:00 ngày 18/09/2026.\n\nObservation từ tool update_application_kanban: {\"status\": \"SUCCESS\", \"message\": \"Job status updated to 'Interviewing'\"}\nHãy tiếp tục suy luận. Nếu đã đủ dữ liệu, trả lời bằng văn bản trực tiếp.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_interview_calendar",
    "arguments": {
      "title": "Phỏng vấn Data Analyst - Vingroup",
      "time": "2026-09-18T14:00:00"
    },
    "observation": {
      "status": "SUCCESS",
      "event_link": "https://calendar.google.com/calendar/event?eid=mock_link",
      "title": "Phỏng vấn Data Analyst - Vingroup",
      "time": "2026-09-18T14:00:00"
    },
    "latency_ms": 819.56
  },
  {
    "step": 4,
    "query": "Hãy xử lý hồ sơ ứng tuyển Data Analyst của tôi tại Vingroup: tra cứu trạng thái, chuyển hồ sơ sang Interviewing nếu phù hợp, rồi đặt lịch phỏng vấn lúc 14:00 ngày 18/09/2026.\n\nObservation từ tool schedule_interview_calendar: {\"status\": \"SUCCESS\", \"event_link\": \"https://calendar.google.com/calendar/event?eid=mock_link\", \"title\": \"Phỏng vấn Data Analyst - Vingroup\", \"time\": \"2026-09-18T14:00:00\"}\nHãy tiếp tục suy luận. Nếu đã đủ dữ liệu, trả lời bằng văn bản trực tiếp.",
    "action_type": "FINAL_ANSWER",
    "thought": "Chuỗi xử lý ứng tuyển đã hoàn tất.",
    "output": "Đã cập nhật hồ sơ sang Interviewing và đặt lịch phỏng vấn Data Analyst tại Vingroup vào 14:00 ngày 18/09/2026.",
    "latency_ms": 955.79
  },
  {
    "step": 1,
    "query": "Hãy tra cứu trạng thái hồ sơ ứng tuyển của tôi tại công ty Không Tồn Tại.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "search_job_status",
    "arguments": {
      "company": "Không Tồn Tại",
      "student_id": "2A202602835"
    },
    "observation": {
      "status": "NOT_FOUND",
      "message": "Không tìm thấy hồ sơ ứng tuyển của sinh viên 2A202602835 tại công ty Không Tồn Tại."
    },
    "latency_ms": 894.89
  },
  {
    "step": 2,
    "query": "Hãy tra cứu trạng thái hồ sơ ứng tuyển của tôi tại công ty Không Tồn Tại.",
    "action_type": "FINAL_ANSWER",
    "thought": "Dừng vì Tool trả về NOT_FOUND.",
    "output": "Không tìm thấy hồ sơ ứng tuyển của sinh viên 2A202602835 tại công ty Không Tồn Tại.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã xác nhận Agent chạy trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công ở lần kiểm tra hiện tại:** 5 / 5 test cases (Mock Provider).
- **Số lượt gọi Tool trong TC04:** 3 lượt; toàn bộ 5 test cases hiện tạo 6 lượt gọi Tool.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!