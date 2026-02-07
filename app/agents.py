import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import Field

# 1. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

# 2. Define the Policy Tool using the BaseTool class
# This is the "Native" way that avoids Pydantic ValidationErrors
class PolicySearchTool(BaseTool):
    name: str = "search_deriv_policy"
    description: str = "Searches the Deriv P2P Policy document for specific security rules."

    def _run(self, query: str) -> str:
        """Internal logic to read the policy file."""
        try:
            path = os.path.join(os.getcwd(), "data", "deriv_policy.txt")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "ERROR: Policy document not found. Please create 'data/deriv_policy.txt'."

# 3. Instantiate the tool
policy_tool = PolicySearchTool()

# 4. Create the Crew Logic
def create_p2p_guardian_crew(chat_history: str, order_details: dict):
    monitor = Agent(
        role='P2P Fraud Monitor',
        goal='Identify suspicious behavior by citing official Deriv Policies',
        backstory=(
            "You are a security expert. You always cross-reference chat logs "
            "with the 'search_deriv_policy' tool to ensure compliance with Deriv rules."
        ),
        llm=llm,
        tools=[policy_tool], # Pass the class instance here
        verbose=True,
        allow_delegation=False
    )

    analysis_task = Task(
        description=(
            f"1. Analyze this chat: '{chat_history}'\n"
            f"2. Use your tool to find relevant rules in the Deriv Policy.\n"
            f"3. Compare with order: {order_details}.\n"
            "4. Return a risk report."
        ),
        expected_output="A structured report citing specific policy rules found in the document.",
        agent=monitor
    )

    return Crew(
        agents=[monitor], 
        tasks=[analysis_task], 
        share_crew=False
    )