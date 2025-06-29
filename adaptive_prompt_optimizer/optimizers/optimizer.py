import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

META_PROMPT_TEMPLATE = """
You are an expert prompt engineer specializing in optimizing user prompts for large language models that power AI coding assistants.

Your task is to rewrite a user's base prompt to make it more effective for a specific target AI tool. You will be given the user's prompt and the internal system prompt of the target tool.

**Target Tool System Prompt:**
---
{system_prompt}
---

**User's Base Prompt:**
---
{base_prompt}
---

**Your Instructions:**

1.  **Analyze:** Carefully analyze the user's base prompt and the target tool's system prompt. Identify the tool's persona, capabilities, constraints, and preferred interaction style.
2.  **Rewrite:** Rewrite the user's prompt. The new prompt should be tailored to the target tool's specific characteristics to elicit the best possible response.
3.  **Explain:** Provide a single-sentence explanation of the most significant change you made and why it improves the prompt for the target tool.
4.  **Score:** Rate the improvement of your optimized prompt over the original on a scale of 1 to 10, where 1 is no improvement and 10 is a breakthrough improvement.

**Output Format:**

Return your response as a single, valid JSON object with the following keys:
- "optimized_prompt": (string) The rewritten, optimized prompt.
- "explanation": (string) Your single-sentence explanation.
- "score": (integer) Your improvement score from 1 to 10.

Do not include any other text, greetings, or explanations outside of the JSON object.
"""


def get_available_tools():
    """
    Loads the list of available tools from the tool_analysis.json file.
    """
    with open('tool_analysis.json', 'r') as f:
        return json.load(f)


def get_system_prompt(system_prompt_file):
    """
    Reads and returns the content of a system prompt file.
    """
    try:
        with open(system_prompt_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def optimize_prompt(base_prompt, tool_id):
    """
    Optimizes a base prompt for a specific tool using the Gemini API.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

    tools = get_available_tools()
    tool_info = next((tool for tool in tools if tool['id'] == tool_id), None)
    
    if not tool_info:
        raise ValueError(f"Tool with id '{tool_id}' not found.")
        
    system_prompt = get_system_prompt(tool_info['system_prompt_file'])
    
    if system_prompt is None or not system_prompt.strip():
        return (
            "Error: System Prompt Not Found or Empty",
            f"The system prompt file for {tool_info['name']} at '{tool_info['system_prompt_file']}' is missing or empty. Please create it and add the tool's system prompt.",
            0
        )

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, convert_system_message_to_human=True)
    parser = JsonOutputParser()
    prompt_template = ChatPromptTemplate.from_template(
        template=META_PROMPT_TEMPLATE
    )
    chain = prompt_template | llm | parser

    try:
        response = chain.invoke({
            "system_prompt": system_prompt,
            "base_prompt": base_prompt
        })
        return response['optimized_prompt'], response['explanation'], response['score']
    except Exception as e:
        error_message = f"An error occurred while communicating with the AI model: {e}"
        return (
            "Error: Optimization Failed",
            error_message,
            0
        ) 