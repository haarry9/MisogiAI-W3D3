import streamlit as st
from optimizers.optimizer import get_available_tools, optimize_prompt

# --- Page Configuration ---
st.set_page_config(
    page_title="Adaptive Prompt Optimizer",
    page_icon="✨",
    layout="wide"
)

# --- State Management ---
if 'optimized_prompt' not in st.session_state:
    st.session_state.optimized_prompt = ""
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'original_prompt' not in st.session_state:
    st.session_state.original_prompt = ""

# --- UI Components ---
st.title("✨ Adaptive Prompt Optimizer")
st.markdown("Optimize your prompts for specific AI coding tools. Select a tool, enter your base prompt, and let the optimizer tailor it for the best results.")

tools = get_available_tools()
tool_names = [tool['name'] for tool in tools]
tool_ids = {tool['name']: tool['id'] for tool in tools}

selected_tool_name = st.selectbox("1. Select Target Tool", options=tool_names)
base_prompt = st.text_area("2. Enter Your Base Prompt", height=150)

if st.button("Optimize Prompt", type="primary"):
    if base_prompt and selected_tool_name:
        selected_tool_id = tool_ids[selected_tool_name]
        with st.spinner(f"Optimizing for {selected_tool_name}..."):
            optimized_prompt, explanation, score = optimize_prompt(base_prompt, selected_tool_id)
            
            # Store results in session state
            st.session_state.original_prompt = base_prompt
            st.session_state.optimized_prompt = optimized_prompt
            st.session_state.explanation = explanation
            st.session_state.score = score
    else:
        st.warning("Please select a tool and enter a prompt.")

# --- Display Results ---
if st.session_state.optimized_prompt:
    st.divider()
    st.subheader("Optimization Results")
    
    st.info(f"**Explanation:** {st.session_state.explanation}")
    st.metric(label="Optimization Score", value=f"{st.session_state.score}/10")

    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Original Prompt", value=st.session_state.original_prompt, height=300, disabled=True)
    with col2:
        st.text_area("✨ Optimized Prompt", value=st.session_state.optimized_prompt, height=300, disabled=True) 