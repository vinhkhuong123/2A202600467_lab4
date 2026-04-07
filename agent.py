
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from tools import search_flights, search_hotels, calculate_budget

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  Cảnh báo: Lỗi khi tải .env: {e}")

# Load system prompt
SYSTEM_PROMPT = ""
try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    print("❌ Lỗi: Không tìm thấy file system_prompt.txt")
    exit(1)
except Exception as e:
    print(f"❌ Lỗi khi đọc system_prompt.txt: {e}")
    exit(1)
# --- 2. Khai báo State ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# --- 3. Khởi tạo LLM và Tools ---

tools_list = [search_flights, search_hotels, calculate_budget]

try:
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools_list)
except Exception as e:
    print(f"❌ Lỗi khi khởi tạo LLM: {e}")
    print("   Kiểm tra OPENAI_API_KEY trong .env")
    exit(1)

# --- 4. Agent Node ---
def agent_node(state: AgentState):
    try:
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm_with_tools.invoke(messages)
        # Debug: Hiển thị khi gọi tools
        if response.tool_calls:
            for tc in response.tool_calls:
                print(f"  🔧 Gọi: {tc['name']}", end="")

        return {"messages": [response]}
    except Exception as e:
        print(f"\n❌ Lỗi trong agent_node: {e}")
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=f"Lỗi: {str(e)}")]}



# --- 5. Xây dựng Graph ---
try:
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)

    tool_node = ToolNode(tools_list)
    builder.add_node("tools", tool_node)

    # --- 5. Xây dựng Edges ---
    # START → agent (bắt đầu với agent)
    builder.add_edge(START, "agent")

    # agent → conditional (kiểm tra có tool_calls không)
    #   - Nếu có tool_calls → chuyển tới tools
    #   - Nếu không có → kết thúc (END)
    builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END,
        }
    )

    # tools → agent (sau khi tools execute, quay lại agent)
    builder.add_edge("tools", "agent")

    graph = builder.compile()
except Exception as e:
    print(f"❌ Lỗi khi xây dựng graph: {e}")
    exit(1)


# --- 6. Chat loop ---
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print("=" * 60)
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    # Maintain conversation history
    conversation_history = []

    while True:
        try:
            user_input = input("\nBạn: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("👋 Tạm biệt! Hẹn gặp lại bạn lần sau!")
                break

            if not user_input:
                continue

            # Add user message to history
            conversation_history.append(("human", user_input))
            
            print("\nTravelBuddy đang suy nghĩ...")
            # Pass full conversation history to agent
            result = graph.invoke({"messages": conversation_history})
            
            # Extract assistant response
            final = result["messages"][-1]
            response_text = final.content if hasattr(final, 'content') else str(final)
            
            print(f"\nTravelBuddy: {response_text}")
            
            # Add assistant response to history
            conversation_history.append(("assistant", response_text))
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! Hẹn gặp lại bạn lần sau!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi trong chat loop: {e}")
            print("   Vui lòng thử lại hoặc gõ 'quit' để thoát")
            continue
