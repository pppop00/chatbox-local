"""
Local AI Chatbox with Gradio Interface
=====================================

A local AI chatbot with streaming responses and dynamic system prompts.
Uses Ollama for local AI processing and Gradio for the web interface.

Features:
- Streaming responses for real-time conversation
- Dynamic system prompts based on user input
- Local processing (zero API costs)
- Web-based chat interface
- Complete privacy (no external data sharing)

Author: Your Name
Model: Llama 3.2 (via Ollama)
Cost: $0 per conversation
"""

import ollama
import gradio as gr

MODEL = "llama3.2"

# Base system message - customize this for your use case
system_message = """You are a helpful AI assistant. You are knowledgeable, friendly, and provide accurate information. Always be polite and helpful in your responses."""

def chat(message, history):
    relevant_system_message = system_message
    if 'belt' in message:
        relevant_system_message += " The store does not sell belts; if you are asked for belts, be sure to point out other items on sale."

    # 构建对话历史，符合 Ollama 的格式
    messages = [{"role": "system", "content": relevant_system_message}]
    messages += history
    messages.append({"role": "user", "content": message})

    # 用 Ollama 的流式响应
    response = ""
    stream = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True  # 开启流式模式
    )

    for chunk in stream:
        delta = chunk.get("message", {}).get("content", "")
        response += delta
        yield response

if __name__ == "__main__":
    # Launch the chat interface
    interface = gr.ChatInterface(fn=chat, type="messages")
    interface.launch()
