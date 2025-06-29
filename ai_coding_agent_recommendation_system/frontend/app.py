import streamlit as st
import requests

st.set_page_config(
    page_title="AI Coding Agent Recommendation System",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #60a5fa 100%);
        color: white;
        border-radius: 8px;
        font-size: 1.1em;
        padding: 0.5em 2em;
        border: none;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #60a5fa 0%, #6366f1 100%);
        color: #fff;
    }
    .agent-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        padding: 1.5em 1.5em 1em 1.5em;
        margin-bottom: 1.5em;
        color: #333;
    }
    .agent-logo {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        margin-right: 1em;
        object-fit: contain;
        background: #f3f4f6;
        padding: 0.3em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 AI Coding Agent Recommendation System")
st.write("""
Enter a description of your coding task and get personalized recommendations for the best AI coding agents!
""")

task = st.text_area("Describe your coding task:", height=120, placeholder="e.g. Generate Python code for a REST API, or Fix a bug in my JavaScript app...")

if st.button("Get Recommendations", type="primary"):
    if not task.strip():
        st.warning("Please enter a task description.")
    else:
        with st.spinner("Analyzing and finding the best agents..."):
            try:
                # Change the backend URL if running elsewhere
                response = requests.post(
                    "http://localhost:8000/recommend",
                    json={"task_description": task},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Top 3 AI Coding Agents for your task:")
                    for agent in data["recommendations"]:
                        col1, col2 = st.columns([1, 6])
                        with col1:
                            # Placeholder logos (replace with real URLs if available)
                            logo_url = ""
                            if agent["name"] == "GitHub Copilot":
                                logo_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                            elif agent["name"] == "Amazon CodeWhisperer":
                                logo_url = "https://d1.awsstatic.com/Developer%20Marketing/codewhisperer/CodeWhisperer_Icon.1b8e6e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e.png"
                            elif agent["name"] == "Cursor":
                                logo_url = "https://avatars.githubusercontent.com/u/120075695?s=200&v=4"
                            elif agent["name"] == "Replit AI":
                                logo_url = "https://replit.com/public/images/favicon-192.png"
                            st.image(logo_url, width=48, caption=" ")
                        with col2:
                            justifications_html = "".join([f"<li>{j}</li>" for j in agent["justifications"]])
                            html_content = f"""
                            <div class='agent-card'>
                                <h4 style='margin-bottom:0.2em;'>{agent['name']}</h4>
                                <span style='color:#6366f1;font-weight:bold;'>Score: {agent['score']}</span>
                                <p style='margin-top:0.5em;'>{agent['description']}</p>
                                <p><b>Strengths:</b> {', '.join(agent["strengths"])}</p>
                                <p><b>Weaknesses:</b> {', '.join(agent["weaknesses"])}</p>
                                <p><b>Platforms:</b> {', '.join(agent["platforms"])}</p>
                                <p><b>Languages:</b> {', '.join(agent["languages"])}</p>
                                <p><b>Features:</b> {', '.join(agent["features"])}</p>
                                <b>Why recommended:</b>
                                <ul>{justifications_html}</ul>
                                <i>{agent['unique']}</i>
                            </div>
                            """
                            st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.error("Backend error: " + response.text)
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

st.markdown("""
---
<small>Made with ❤️ using Streamlit & FastAPI</small>
""")
