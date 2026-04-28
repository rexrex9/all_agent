import asyncio
from contextlib import AsyncExitStack
import os

# Try to get project ID for Vertex AI, fallback if not available
try:
    import google.auth
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    # Set a default location if needed, adjust as necessary
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
    print(f"Using Vertex AI project: {project_id}")
except Exception:
    project_id = None
    print("Vertex AI project ID not found, Google GenAI API may be used if GOOGLE_API_KEY is set.")


from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

# --- Agent Definition ---
async def create_agent():
    """Creates an ADK Agent connected to the local PowerPoint MCP Server."""
    common_exit_stack = AsyncExitStack()

    mcp_server_url = "http://127.0.0.1:8000/sse"

    print(f"Attempting to connect to PowerPoint MCP server at {mcp_server_url}...")
    try:
        # Connect to the local MCP server via SSE
        tools, _ = await MCPToolset.from_server(
            connection_params=SseServerParams(
                url=mcp_server_url
                # No project_id or location needed for local, unauthenticated SSE
                # No specific headers needed unless your server requires them
            ),
            async_exit_stack=common_exit_stack
        )
        print(f"Successfully connected to {mcp_server_url}. Fetched {len(tools)} tools.")
    except Exception as e:
        print(f"FATAL: Error connecting to MCP server at {mcp_server_url}: {e}")
        print("Please ensure the MCP server (server.py) is running.")
        # Re-raise the exception to prevent the agent from starting incorrectly
        raise ConnectionError(f"Could not connect to MCP Server at {mcp_server_url}: {e}") from e

    # Define the agent
    # Using a model capable of understanding images is recommended for visual verification
    agent_model = 'gemini-2.5-pro-preview-03-25' 
    print(f"Initializing agent with model: {agent_model}")

    agent = LlmAgent(
        model=agent_model,
        name='presentation_designer_pro',
        instruction=(
            "You are a meticulous presentation designer assistant. Your primary goal is to create "
            "visually appealing and accurate PowerPoint slides based on user requests using the provided tools "
            "(like add_slide, add_textbox, add_shape, add_picture, etc.).\n"
            "\n"
            "**Crucially:** After making significant visual changes (like adding shapes, text formatting, placing pictures), "
            "you **MUST** verify the slide's appearance. Use the `get_slide_image` tool to render the affected slide. "
            "Analyze the returned image carefully and describe its key elements (positions, text content, overall layout) "
            "back to the user for confirmation. Only proceed once you are confident the slide looks correct. "
            "Don't just rely on the text description tool (`get_slide_content_description`); visual proof is required. "
            "State clearly that you are performing visual verification when using `get_slide_image`.\n"
            "If the image rendering tool fails, inform the user and rely on the description tool instead, noting the limitation."
        ),
        tools=tools, # Provide the MCP tools fetched from the server
    )
    print(f"Agent '{agent.name}' created successfully.")
    return agent, common_exit_stack

# --- Root Agent Assignment for adk web ---
# This runs the async function to get the agent and exit_stack when the module is loaded
# NOTE: This approach works for `adk web`. For standalone scripts, manage the event loop and cleanup differently.
root_agent = create_agent()
print("Agent definition complete. Ready for adk web.")
