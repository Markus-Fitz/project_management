# pm_mcp.py
# MCP server using HTTP/SSE transport.
# Exposes project management commands as tools callable by an LLM.
#
# Start with:
#   python pm_mcp.py
# Server will be available at http://0.0.0.0:5173
# For local-only access change host to "127.0.0.1"

import json
import sys
from pathlib import Path
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent, CallToolResult, ListToolsResult
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
import uvicorn


# ── Import your actual command functions ──────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent / "pm_src"))
from commands import initialize_project , add_task, add_task_hours, add_note_hours, add_research_note#, mark_task_done, add_research_note, add_supplier, add_purchase

# ── Server configuration ──────────────────────────────────────────────────────
HOST = "0.0.0.0"   # accepts connections from any machine on the network
                    # change to "127.0.0.1" to restrict to local machine only
PORT = 5173

# ── Create the MCP server instance ───────────────────────────────────────────
server = Server("project-manager")


# ── Tool definitions ──────────────────────────────────────────────────────────
# Each tool has:
#   name        → what the LLM calls it
#   description → what the LLM reads to decide when to use it
#   inputSchema → what arguments it accepts (JSON Schema)

TOOLS = [
    Tool(
        name="initialize_project",
        description="Create a new project from a template. Call when the user wants to start a new project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Human readable project name"
                },
                "template_name": {
                    "type": "string",
                    "description": "Template folder to use: Template_development for a hardware or programming project or a project with hard deadlines and a necessary outcome - Template_research for a resarch-focused project.",
                    "enum": ["Template_development", "Template_research"]
                }
            },
            "required": ["project_name", "template_name"]
        }
    ),

    Tool(
        name="add_task",
        description="Add a new task to an existing project. Use for hardware or software development or anything where fixed deadlines or results are expected.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Name of the project in which to create the task"
                },
                "task_name": {
                    "type": "string",
                    "description": "Short descriptive title for the task"
                }
            },
            "required": ["task_name", "project_name"]
        }
    ),

    Tool(
        name="add_task_hours",
        description="Adds hours to an existing task in a specified project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Name of the project in which the task is located"
                },
                "task_name": {
                    "type": "string",
                    "description": "Title for the task"
                },
                "hours": {
                    "type": "string",
                    "description": "Amount of hours to add to the task in decimal format (e.g. 1.5 means 1 hour 30 min)."
                }
            },
            "required": ["task_name", "project_name", "hours"]
        }
    ),

    Tool(
        name="add_note_hours",
        description="Adds hours to an existing research note in a specified project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "Name of the project in which the note is located"
                },
                "note_name": {
                    "type": "string",
                    "description": "Title for the task"
                },
                "hours": {
                    "type": "string",
                    "description": "Amount of hours to add to the note in decimal format (e.g. 1.5 means 1 hour 30 min)."
                }
            },
            "required": ["note_name", "project_name", "hours"]
        }
    ),

    Tool(
        name="add_research_note",
        description="Add a new research note to a research project. Use for papers, ideas, or observations with no specific outcome or deadline in mind.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The project id the note belongs to"
                },
                "note_name": {
                    "type": "string",
                    "description": "Title of the note or paper"
                }
            },
            "required": ["project_name", "note_name"]
        }
    ),
]


# ── Tool registry ─────────────────────────────────────────────────────────────
# Maps tool name → actual Python function.
# When the LLM requests a tool call, handle_call_tool looks it up here.

TOOL_REGISTRY = {
    "initialize_project":       initialize_project,
    "add_task":                 add_task,
    "add_note_hours":           add_note_hours,
    "add_task_hours":           add_task_hours,
    #"mark_task_done":           mark_task_done,
    "add_research_note":        add_research_note,
    #"add_supplier":             add_supplier,
    #"add_purchase":             add_purchase
}


# ── MCP protocol handlers ─────────────────────────────────────────────────────

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """
    Called by the client on connection to discover available tools.
    Simply returns the TOOLS list defined above.
    """
    return ListToolsResult(tools=TOOLS)


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """
    Called when the LLM requests a tool execution.
    Looks up the function in TOOL_REGISTRY, calls it, returns the result.
    """

    # Check the tool exists
    if name not in TOOL_REGISTRY:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            isError=True
        )

    # Call the actual Python function with the arguments the LLM provided
    try:
        result = TOOL_REGISTRY[name](**arguments)
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )

    # Return errors to the LLM as readable messages rather than crashing
    except TypeError as e:
        # Catches wrong/missing arguments
        return CallToolResult(
            content=[TextContent(type="text", text=f"Argument error: {str(e)}")],
            isError=True
        )
    except Exception as e:
        # Catches anything from your command functions (file not found etc.)
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )


# ── HTTP/SSE server setup ─────────────────────────────────────────────────────

sse_transport = SseServerTransport("/messages")

async def handle_sse(request: Request):
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0],
            streams[1],
            server.create_initialization_options()
        )

app = Starlette(routes=[
    Route("/sse",      endpoint=handle_sse),
    Mount("/messages", app=sse_transport.handle_post_message),
])

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)