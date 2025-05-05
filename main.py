import streamlit as st
from PyPDF2 import PdfReader
import os
import re
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize IBM Granite model credentials
credentials = Credentials(url=WATSONX_URL, api_key=WATSONX_API_KEY)
model_id = "ibm/granite-3-8b-instruct"

# Function to clean extracted PDF text
def clean_pdf_text(text):
    text = re.sub(r'(\d+\.\n)', r'\1__PRESERVE_NEWLINE__', text)
    text = re.sub(r'(●\n)', r'\1__PRESERVE_NEWLINE__', text)
    text = re.sub(r'(○\n)', r'\1__PRESERVE_NEWLINE__', text)
    text = re.sub(r'\n+', ' ', text)
    text = text.replace('__PRESERVE_NEWLINE__', '\n')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to summarize document using Granite
def summarize_document(cleaned_text):
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 550,  # Approx. 450 words
        "min_new_tokens": 0,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "repetition_penalty": 1
    }
    prompt = (
        "You are an AI Brainstorming Buddy powered by IBM Granite. Analyze the following business meeting notes related to soap marketing. "
        "Summarize the key information in a concise, structured format using bullet points, optimized for further brainstorming. Include:\n\n"
        "- What the Meeting Highlights About: Key themes, focus areas, or insights from the discussion (e.g., branding trends, target audience preferences, or promotional opportunities).\n"
        "- Key Discussion Points: Main issues or topics discussed, in brief.\n"
        "- Decisions Made: Any conclusions or agreements reached, in brief.\n"
        "- Action Items: Specific tasks assigned or next steps, in brief.\n"
        "- Important Insights: Key takeaways relevant to soap marketing, in brief.\n\n"
        "Limit the summary to a maximum of 200 words. Use concise, actionable points that are clear and suitable for brainstorming marketing strategies. "
        "Text to summarize: {cleaned_text}"
        "start by Summary:"
    ).format(**{"cleaned_text": cleaned_text})
    try:
        model = ModelInference(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID
        )
        summary = model.generate_text(prompt=prompt, guardrails=True)
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Function to get AI response from Granite model
def get_ai_response(user_question, thinking_mode=None, chat_history=None):
    # Initialize model with mode-specific parameters
    if thinking_mode:
        # Get document summary from session state at the beginning
        document_summary = st.session_state.get("document_summary", "")
        
        if thinking_mode == "Creative":
            parameters = {
                "decoding_method": "sample",
                "max_new_tokens": 300,
                "min_new_tokens": 0,
                "temperature": 1.2,
                "top_k": 75,
                "top_p": 1.0,
                "repetition_penalty": 1
            }
            prompt = f"""
                You are an AI Brainstorming Buddy powered by IBM Granite.

                Below is a concise summary of the user’s document:
                {document_summary if document_summary else "No summary provided."}

                Task:
                Based on the above summary, suggest just one highly creative and original idea in response to the following question:

                “{user_question}”

                Instructions:
                - Present your idea in a conversational, friendly, and professional tone.
                - Naturally explain your thinking in 4–5 sentences, as if you’re chatting with the user and inviting their thoughts.
                - Highlight how your idea addresses the user’s needs.
                - Keep the whole response under 70 words.

                Instead of a structured format, speak as if you’re brainstorming with the user and open to further discussion.
            """
        elif thinking_mode == "Diverse":
            parameters = {
                "decoding_method": "sample",
                "max_new_tokens": 300,
                "min_new_tokens": 0,
                "temperature": 0.9,
                "top_k": 60,
                "top_p": 0.9,
                "repetition_penalty": 1
            }
            prompt = (
                "You are an AI Brainstorming Buddy powered by IBM Granite.\n"
                "Below is a concise summary of the user’s document:\n"
                f"{document_summary if document_summary else 'No summary provided.'}\n\n"
                "Task:\n"
                "Drawing from the summary, suggest just one practical idea for the user’s question that thoughtfully considers one of the diverse and multiple perspectives (e.g., different stakeholders, scenarios, or approaches, etc):\n"
                f"“{user_question}”\n\n"
                "Instructions:\n"
                "- Share your idea in a friendly, conversational tone, as if you’re discussing options with the user.\n"
                "- Explain within 10 sentences how you weighed different viewpoints and why this idea might work well from several angles.\n"
                "- Invite the user to share their own perspective or ask questions.\n"
                "- Keep the response under 100 words.\n\n"
                "Instead of a structured format, speak as if you’re brainstorming with the user and open to further discussion."
            )
        elif thinking_mode == "Lateral":
            parameters = {
                "decoding_method": "sample",
                "max_new_tokens": 300,
                "min_new_tokens": 0,
                "temperature": 1.0,
                "top_k": 30,
                "top_p": 1.0,
                "repetition_penalty": 1
            }
            prompt = (
                "You are an AI Brainstorming Buddy powered by IBM Granite.\n"
                "Below is a concise summary of the user’s document:\n"
                f"{document_summary if document_summary else 'No summary provided.'}\n\n"
                "Task:\n"
                "Based on the above summary, suggest one unique idea for the user’s question using the SCAMPER technique (Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse). Choose the most relevant SCAMPER action and apply it creatively:\n"
                f"“{user_question}”\n\n"
                "Instructions:\n"
                "- Weave the SCAMPER action you’re using naturally into your conversational explanation, without labeling it explicitly.\n"
                "- Present your idea in a friendly, professional tone, as if you’re brainstorming together.\n"
                "- In 8–10 sentences, explain how you came up with the idea and why it addresses the user’s needs, keeping the tone open and engaging.\n"
                "- Keep the response under 100 words.\n\n"
                "Avoid any headings, bullet points, or structured formatting-just a clear, natural conversation that invites the user to discuss or ask questions."

            )
    else:
        # Mode B: Conversational
        parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 150,
            "min_new_tokens": 0,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1
        }
        previous_messages = ""
        if chat_history and len(chat_history) >= 2:
            previous_messages = f"User: {chat_history[-2]['content']}\nAssistant: {chat_history[-1]['content']}"
        prompt = (
            "You are a conversational AI Brainstorming Assistant. Clarify or elaborate on the user’s question: {user_question}, "
            "using the following previous message pair for context: {previous_messages}. "
            "Provide a clear, concise response within 100–200 words to deepen the discussion."
        ).format(**{"user_question": user_question, "previous_messages": previous_messages if previous_messages else "No previous messages"})

    # Initialize and call Granite model
    try:
        model = ModelInference(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID
        )
        response = model.generate_text(prompt=prompt, guardrails=True)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Sidebar configuration
with st.sidebar:
    st.markdown("""
    <style>
        .sidebar-container {
            background-color: #1C2526;
            padding: 20px;
            height: 100vh;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        .app-title {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 20px;
            border-bottom: 2px solid #4e5bff;
            padding-bottom: 10px;
        }
        .welcome-section {
            font-size: 18px;
            color: #ffffff;
            margin-bottom: 10px;
        }
        .welcome-text {
            font-size: 14px;
            color: #b0b0b0;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        .thinking-modes {
            background-color: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .mode-title {
            font-size: 16px;
            color: #ffffff;
            margin-bottom: 10px;
        }
        .mode-item {
            font-size: 14px;
            color: #4e5bff;
            margin: 5px 0;
        }
        .mode-desc {
            font-size: 12px;
            color: #b0b0b0;
            margin-left: 10px;
        }
        .upload-section {
            font-size: 16px;
            color: #ffffff;
            margin-bottom: 10px;
        }
        .upload-text {
            font-size: 12px;
            color: #b0b0b0;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="app-title">AI Brainstorming Buddy</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-section">Welcome</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Your intelligent companion for creative ideation and problem-solving. Explore ideas from multiple angles and discover innovative solutions to your challenges.</div>', unsafe_allow_html=True)
    st.markdown('<div class="thinking-modes"><div class="mode-title">Thinking Modes</div>', unsafe_allow_html=True)
    st.markdown('<div class="mode-item">Creative<span class="mode-desc">Innovative, out-of-the-box ideas</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="mode-item">Diverse<span class="mode-desc">Multiple perspectives and approaches</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="mode-item">Lateral<span class="mode-desc">Unexpected connections and insights</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-section">Document Upload</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-text">Upload PDFs, text files, or documents to reference during brainstorming session.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select Files", type=["pdf", "txt"], accept_multiple_files=False, label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.markdown(f'<div class="upload-text">Uploaded File: {uploaded_file.name}</div>', unsafe_allow_html=True)
        if st.button("Process Document"):
            with st.spinner("Processing and summarizing..."):
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                cleaned_text = clean_pdf_text(text)
                summary = summarize_document(cleaned_text)
                st.session_state.document_summary = summary
                st.success("Document processed and summarized!")
                # Display summary for debugging
                with st.expander("View Document Summary"):
                    st.write(summary)

# Chat section CSS
st.markdown("""
<style>
    html, body {
        overflow: hidden;
        margin: 0;
        padding: 0;
        height: 100vh;
    }
    .main {
        background: linear-gradient(180deg, #1C2526 0%, #0F1415 100%);
        height: 100vh;
        padding: 15px;
        padding-bottom: 40px;
        overflow-y: auto;
    }
    .stChatMessage {
        max-width: 100%;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.4;
        margin-bottom: 8px;
        white-space: pre-wrap;
        position: relative;
    }
    .stChatMessage.user {
        background-color: #4e5bff;
        color: #ffffff;
        margin-left: auto;
        text-align: right;
    }
    .stChatMessage.assistant {
        background-color: #2a2a2a;
        color: #ffffff;
        margin-right: auto;
    }
    .stChatMessage.assistant.creative {
        border: 2px solid #ff6f61 !important;
    }
    .stChatMessage.assistant.creative::before {
        content: "Creative Thinking";
        display: block;
        font-size: 12px;
        color: #ff6f61;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .stChatMessage.assistant.diverse {
        border: 2px solid #4e5bff !important;
    }
    .stChatMessage.assistant.diverse::before {
        content: "Diverse Thinking";
        display: block;
        font-size: 12px;
        color: #4e5bff;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .stChatMessage.assistant.lateral {
        border: 2px solid #28a745 !important;
    }
    .stChatMessage.assistant.lateral::before {
        content: "Lateral Thinking";
        display: block;
        font-size: 12px;
        color: #28a745;
        margin-bottom: 5px;
        font-weight: bold;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="creative_btn"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="diverse_btn"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="lateral_btn"] {
        background: linear-gradient(135deg, rgba(50, 50, 50, 0.7), rgba(30, 30, 30, 0.7)) !important;
        color: #e0e0e0 !important;
        border: none !important;
        padding: 3px 6px !important;
        border-radius: 25px !important;
        font-size: 10px !important;
        font-family: 'Helvetica', sans-serif !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        gap: 2px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 1px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        backdrop-filter: blur(5px) !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="creative_btn"]:hover,
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="diverse_btn"]:hover,
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="lateral_btn"]:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, rgba(70, 70, 70, 0.7), rgba(50, 50, 50, 0.7)) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="creative_btn"][data-selected="true"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="diverse_btn"][data-selected="true"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="lateral_btn"][data-selected="true"] {
        background: linear-gradient(135deg, rgba(90, 110, 255, 0.9), rgba(70, 90, 220, 0.9)) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="creative_btn"] span,
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="diverse_btn"] span,
    div[data-testid="stHorizontalBlock"] button[kind="primary"][key="lateral_btn"] span {
        font-size: 8px !important;
    }
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = None
if "document_summary" not in st.session_state:
    st.session_state.document_summary = ""

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "thinking_mode" in message and message["thinking_mode"] is not None:
            thinking_mode_class = message["thinking_mode"].lower()
            st.markdown(f'<div class="{thinking_mode_class}">', unsafe_allow_html=True)
        st.markdown(message["content"])
        if message["role"] == "assistant" and "thinking_mode" in message and message["thinking_mode"] is not None:
            st.markdown('</div>', unsafe_allow_html=True)

# Thinking mode buttons
col_buttons, col_empty = st.columns([1, 1], gap="small")
with col_buttons:
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    with col1:
        creative_selected = st.session_state.thinking_mode == "Creative"
        if st.button("💡 Creative", key="creative_btn", use_container_width=True, help="Innovative, out-of-the-box ideas"):
            st.session_state.thinking_mode = "Creative" if st.session_state.thinking_mode != "Creative" else None
    with col2:
        diverse_selected = st.session_state.thinking_mode == "Diverse"
        if st.button("🌐 Diverse", key="diverse_btn", use_container_width=True, help="Multiple perspectives and approaches"):
            st.session_state.thinking_mode = "Diverse" if st.session_state.thinking_mode != "Diverse" else None
    with col3:
        lateral_selected = st.session_state.thinking_mode == "Lateral"
        if st.button("🔍 Lateral", key="lateral_btn", use_container_width=True, help="Unexpected connections and insights"):
            st.session_state.thinking_mode = "Lateral" if st.session_state.thinking_mode != "Lateral" else None
with col_empty:
    pass

# Update button states
st.markdown(f"""
<script>
    document.querySelector("button[kind='primary'][key='creative_btn']").setAttribute('data-selected', {str(creative_selected).lower()});
    document.querySelector("button[kind='primary'][key='diverse_btn']").setAttribute('data-selected', {str(diverse_selected).lower()});
    document.querySelector("button[kind='primary'][key='lateral_btn']").setAttribute('data-selected', {str(lateral_selected).lower()});
</script>
""", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Generating response..."):
        ai_response = get_ai_response(user_input, st.session_state.thinking_mode, st.session_state.chat_history)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": ai_response,
        "thinking_mode": st.session_state.thinking_mode
    })
    st.session_state.thinking_mode = None
    st.rerun()



# Auto-scroll chat area
st.markdown("""
<script>
    const chatArea = document.querySelector('.main');
    if (chatArea) {
        const observer = new MutationObserver(() => {
            chatArea.scrollTop = chatArea.scrollHeight;
        });
        observer.observe(chatArea, { childList: true, subtree: true });
        chatArea.scrollTop = chatArea.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)

