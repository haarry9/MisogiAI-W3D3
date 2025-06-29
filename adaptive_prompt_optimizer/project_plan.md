# Adaptive Prompt Optimizer - Project Plan

This document outlines the phased implementation plan for the Adaptive Prompt Optimizer tool.

### **Phase 1: Project Setup & Foundation**

This phase focuses on creating the skeleton of our application, setting up dependencies, and preparing for the core logic.

1.  **Directory Structure**: Create the necessary files and directories.
    - `app.py`
    - `optimizers/`
    - `optimizers/prompts/`
    - `tool_analysis.json`
    - `README.md`
    - `requirements.txt`
    - `.env.example`
2.  **Dependencies**: Create a `requirements.txt` file with the necessary Python libraries: `streamlit`, `langchain`, `langchain-google-genai`, and `python-dotenv`.
3.  **Configuration**: Create a `.env.example` file to guide the user in setting up their `GOOGLE_API_KEY`.
4.  **Tool Metadata**: Create `tool_analysis.json` and populate it with initial data for a few tools (e.g., Cursor, Replit) to establish the data structure. The structure will include `id`, `name`, `description`, and `system_prompt_file`.
5.  **Initial Files**: Create the initial versions of `app.py` and a new `optimizers/optimizer.py` module with placeholder content.

---

### **Phase 2: Core Logic Implementation**

This phase involves building the backend engine that powers the prompt optimization.

1.  **Data Loading**: In `optimizers/optimizer.py`, implement a function to read and parse `tool_analysis.json` to get the list of available tools.
2.  **Prompt Loading**: Implement a utility function to read the content of a specified system prompt file from the `optimizers/prompts/` directory.
3.  **LLM-Powered Optimization Engine**:
    - Implement the main optimization function in `optimizers/optimizer.py`.
    - This function will accept the user's base prompt and the ID of the target tool.
    - It will construct a "meta-prompt" to be sent to the Google Gemini model. This meta-prompt will instruct Gemini to:
        - Act as an expert prompt engineer.
        - Analyze the provided base prompt and the target tool's system prompt.
        - Rewrite the base prompt to be optimal for the target tool, considering its persona, capabilities, and constraints.
        - Generate a brief, one-sentence explanation of the key optimization strategy applied.
        - Provide a "success score" (e.g., a rating out of 10) indicating how much better the new prompt is.
    - Use the `langchain` and `langchain-google-genai` libraries to execute the call to the Gemini API.
    - Implement logic to parse the structured response (optimized prompt, explanation, score) from the Gemini model.

---

### **Phase 3: Frontend Implementation (Streamlit)**

This phase focuses on building the user interface.

1.  **UI Layout**: In `app.py`, build the Streamlit interface with the following components:
    - A title: "Adaptive Prompt Optimizer".
    - A dropdown menu populated with the names of the tools from `tool_analysis.json`.
    - A text area for the user to input their base prompt.
    - An "Optimize" button to trigger the process.
    - A clear "Before vs. After" comparison layout using `st.columns`.
    - A section to display the AI-generated explanation for the optimization.
    - A section to display the AI-generated success score.
2.  **Backend Integration**:
    - On button click, call the core optimization function from `optimizers/optimizer.py`.
    - Pass the selected tool and the user's input prompt.
    - Display the results (optimized prompt, explanation, score) in the designated UI areas.
    - Manage application state to handle user input and display outputs smoothly.

---

### **Phase 4: Populating System Prompts**

This phase involves sourcing the raw data required for the optimization engine.

1.  **Create Placeholder Files**: Create the necessary text files in `optimizers/prompts/` (e.g., `cursor.txt`, `replit.txt`) as defined in `tool_analysis.json`.
2.  **Manual Data Entry**: The user will be prompted to manually copy and paste the system prompts for each tool from the [CLARiTAS GitHub repository](https://github.com/jayinc/CLARiTAS) into the corresponding files.

---

### **Phase 5: Refinement and Testing**

This final phase focuses on improving the robustness and usability of the tool.

1.  **Iterative Testing**: Test the full workflow with a variety of base prompts and target tools to ensure the quality of the optimizations.
2.  **Meta-Prompt Engineering**: Refine the meta-prompt sent to Gemini based on test results to improve the consistency and quality of its output.
3.  **Error Handling**: Implement robust error handling for potential issues such as:
    - Missing `GOOGLE_API_KEY`.
    - System prompt files not found.
    - Failures in the Gemini API call.
    - Unexpected response format from the API.
4.  **Code Cleanup**: Refactor the code for clarity, add comments where the logic is complex, and ensure the project structure remains clean and maintainable. 