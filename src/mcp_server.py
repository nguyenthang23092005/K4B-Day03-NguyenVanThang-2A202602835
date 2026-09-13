"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPJobApplicationServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "smart-job-application-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        [TASK 2.1] HỌC VIÊN HOÀN THIỆN HÀM THỰC THI TOOL TRÊN MCP SERVER
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC
        """
        raw_result = dispatch_tool_call(tool_name, arguments)
        content = json.loads(raw_result)
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }
if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (smart-job-application-mcp-server)")
    print("==========================================================")
    
    server = MCPJobApplicationServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    test_result = server.call_tool("search_job_status", {
        "company": "Vingroup",
        "student_id": "2A202602835"
    })
    if not test_result:
        print("⏳ [MCP CHECK]: call_tool() chưa trả về dữ liệu.")
    else:
        print("✅ [MCP CHECK]: Test dispatch tool 'search_job_status' thành công:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
