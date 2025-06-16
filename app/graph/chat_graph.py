from typing import Dict, TypedDict, List, Annotated, Literal
import time
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models.llm_models import get_model
from app.models.memory import get_vector_chat_history, get_mongodb_chat_history
from app.models.vector_store import get_vector_store
from app.utils.langsmith import get_langchain_tracer
from app.config.config import LANGSMITH_TRACING
from app.enum.model import ModelProvider, ModelGeminiName, ModelOpenAiName

# Define state types
class AgentState(TypedDict):
    messages: List[BaseMessage]

def create_chat_graph(session_id, model_provider: ModelProvider = ModelProvider.GEMINI, model_name: ModelGeminiName = ModelGeminiName.GEMINI_2_0_FLASH, temperature=0.7, max_tokens=200):
    """
    Create a simplified version of a conversation agent.
    
    Args:
        session_id (str): A unique identifier for the conversation
        model_provider (str): The LLM provider to use ('openai' or 'gemini')
        model_name (str, optional): The specific model name to use
        temperature (float): Controls randomness in responses
        max_tokens (int): Maximum number of tokens in the response (default: 150)
        
    Returns:
        A function that processes messages
    """
    # Configure model parameters
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens  # Add max_tokens parameter
    }
    
    if model_provider == ModelProvider.OPENAI:
        model_name = ModelOpenAiName.OPENAI_GPT_4_1_NANO
    
    # Convert enum to string value if it's an enum
    model_name_value = model_name.value if hasattr(model_name, 'value') else model_name
    
    if model_name_value:
        model_kwargs["model_name"] = model_name_value
    
    # Run name for tracing
    run_name = f"{model_provider}-graph-chat-{session_id}"
    
    # Get the language model
    llm = get_model(provider=model_provider, run_name=run_name, **model_kwargs)
    
    # Create the prompt template - handle differently based on model provider
    if model_provider == ModelProvider.GEMINI:
        # For Gemini, we'll use a simple messages placeholder
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="messages"),
        ])
    elif model_provider == ModelProvider.OPENAI:
        # For OpenAI, we'll also use a simple messages placeholder
        # System message is already added in process_user_input
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="messages"),
        ])
    
    # Define the process function
    def process_messages(messages):
        # For Gemini model and empty conversation, add system instruction to first message
        if model_provider == ModelProvider.GEMINI:
            # Kiểm tra xem đã có SystemMessage chưa
            has_system_message = any(isinstance(msg, SystemMessage) for msg in messages)
            
            # Không cần thêm system prompt nữa vì đã được xử lý trong process_user_input
            # Chỉ giữ lại việc kiểm tra để đảm bảo tương thích ngược
            if not has_system_message and not messages:
                # Trường hợp hiếm gặp: không có tin nhắn nào và không có system message
                messages.append(SystemMessage(content="You are a friendly and helpful HSK chatbot assistant."))
        
        # Get the response from the LLM
        response = prompt.invoke({"messages": messages})
        # Don't pass callbacks here as they're already included in the model
        chain_response = llm.invoke(response)
        
        # Create a new AI message
        ai_message = AIMessage(content=chain_response.content)
        
        # Return the updated messages (không lưu vào message_history nữa vì đã xử lý trong process_user_input)
        return messages + [ai_message]
    
    return process_messages

def process_user_input(graph_function, user_input, session_id, similarity_threshold=0.6):
    """
    Process user input through the graph function.
    
    Args:
        graph_function: The function that processes messages
        user_input (str): The user's input message
        session_id (str): The session ID for retrieving history
        similarity_threshold (float): Minimum similarity score (0.0 to 1.0) for vector search
        
    Returns:
        str: The assistant's response
    """
    # Lấy 10 tin nhắn gần nhất từ MongoDB
    mongodb_history = get_mongodb_chat_history(session_id, max_messages=4)
    
    recent_messages = mongodb_history.messages
    
    # Lấy vector store để tìm kiếm các tin nhắn tương tự từ qdrant
    vector_store = get_vector_store(collection_name="chat_messages")
    
    # Tìm 5 tin nhắn người dùng (human) tương tự nhất
    similar_human_messages = vector_store.search_similar_messages(
        query=user_input,
        session_id=session_id,
        k=5,
        filter_type="human",
        score_threshold=similarity_threshold
    )
    
    # Tìm 5 tin nhắn AI tương tự nhất
    similar_ai_messages = vector_store.search_similar_messages(
        query=user_input,
        session_id=session_id,
        k=5,
        filter_type="ai",
        score_threshold=similarity_threshold
    )
    
    # Tạo system message với thông tin về các tin nhắn tương tự
    system_prompt = """Bạn là một AI đóng vai nhân vật với các thông tin sau:
1. **Tên**: mIA
2. **Nghề nghiệp**: Giáo viên tiếng Trung
3. **Vai trò**: Hỗ trợ người học về lí thuyết, từ vựng, ngữ pháp, giải thích các câu hỏi của người dùng
4. **Tính cách**: Thân thiện, học hỏi, chuyên nghiệp, không ngại khó khăn
5. **Ngôn ngữ**: Tiếng Việt, Tiếng Trung, Tiếng Anh

**Kỳ vọng dành cho bạn**:
- Khi trả lời, tập trung vào duy nhất một vấn đề hoặc câu hỏi quan trọng nhất mà tôi đưa ra.
- Chủ động dự đoán tình huống và phản ứng linh hoạt, tự nhiên theo diễn biến cuộc trò chuyện.
- Đảm bảo tính nhất quán trong cách hành xử, ngôn ngữ và cảm xúc xuyên suốt toàn bộ cuộc trò chuyện.
**Ghi chú**:
- Bởi vì bạn luôn được bổ sung context lưu lại lịch sử mà tôi đã hỏi để ghi nhớ thông tin trước đó, khi trả lời hoặc xử lý yêu cầu hiện tại, hãy ưu tiên tham khảo và sử dụng toàn bộ lượng thông tin đã lưu trong context này. 
- Điều này giúp đảm bảo câu trả lời luôn nhất quán, tránh lặp lại thông tin tôi đã biết và cung cấp phản hồi chính xác, tự nhiên, phù hợp nhất với ngữ cảnh cũng như trải nghiệm trước đây của tôi. 
- Trong trường hợp thông tin hiện tại chưa rõ ràng hoặc chưa đầy đủ, hãy chủ động khai thác thông tin từ context lịch sử để làm rõ và hoàn thiện câu trả lời.
**Quan trọng**:
- Trả lời linh hoạt theo ngôn ngữ mà người dùng đã nói, không được trả lời bằng ngôn ngữ khác.
- Nội dung không được vượt quá 100 từ.
### Hãy bắt đầu cuộc trò chuyện với sự nhập vai chân thực nhất!
"""

    # Thêm thông tin về các tin nhắn tương tự từ người dùng và AI
    if similar_human_messages or similar_ai_messages:
        system_prompt += "\n\nInformation about user questions and previous AI answers:"
        
        # Thêm các tin nhắn người dùng tương tự
        if similar_human_messages:
            system_prompt += "\n- Questions:"
            for msg in similar_human_messages:
                if hasattr(msg, 'content'):
                    system_prompt += f"\n+ {msg.content}"
        
        # Thêm các tin nhắn AI tương tự
        if similar_ai_messages:
            system_prompt += "\n- AI:"
            for msg in similar_ai_messages:
                if hasattr(msg, 'content'):
                    system_prompt += f"\n+ {msg.content}"
    
    # Tạo messages mới với system message chứa context
    messages = []
    
    # Thêm system message vào đầu
    messages.append(SystemMessage(content=system_prompt))
    
    # Thêm 10 tin nhắn gần nhất từ MongoDB vào bối cảnh
    if recent_messages:
        messages.extend(recent_messages)
    
    # Thêm tin nhắn mới của người dùng
    human_message = HumanMessage(content=user_input)
    mongodb_history.add_message(human_message)
    
    # Thêm tin nhắn vào vector store
    vector_store.add_message(human_message, session_id, {"timestamp": int(time.time())})
    
    messages.append(human_message)
    
    # Xử lý tin nhắn qua graph function
    updated_messages = graph_function(messages)
    
    # Lấy tin nhắn cuối cùng (phản hồi của assistant)
    last_message = updated_messages[-1] if updated_messages else None
    
    if last_message and hasattr(last_message, 'content'):
        # Lưu phản hồi của assistant vào MongoDB history
        mongodb_history.add_message(last_message)
        
        # Lưu phản hồi của assistant vào vector store
        vector_store.add_message(last_message, session_id, {"timestamp": int(time.time())})
        return {"output": last_message.content}
    
    return {"output": "I'm sorry, I couldn't generate a response."} 