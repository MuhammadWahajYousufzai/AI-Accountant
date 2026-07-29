from agents import Agent, Runner, RunConfig
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from app.core.config import settings


class AgentContext:
    def __init__(self, user_id: str, db_session_factory):
        self.user_id = user_id
        self.db_session_factory = db_session_factory


_gemini_client = None
_gemini_model = None


def get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = AsyncOpenAI(
            api_key=settings.google_api_key,
            base_url=settings.gemini_base_url,
        )
    return _gemini_client


def get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        _gemini_model = OpenAIChatCompletionsModel(
            openai_client=get_gemini_client(),
            model=settings.gemini_model,
        )
    return _gemini_model


def create_triage_agent(expense_agent, income_agent, report_agent, audit_agent, query_agent) -> Agent:
    return Agent[AgentContext](
        name="Triage",
        instructions="""You are the smart triage layer of an AI accounting assistant. Your job: understand the user's intent and hand off to the right specialist immediately.

ROUTING RULES:
- Expenses → Expense Agent: creating, listing, searching, updating, deleting expenses
- Income → Income Agent: creating, listing, searching, updating, deleting income
- Reports/Summaries → Report Agent: profit & loss, balance sheet, financial overview, dashboard data
- Audit/Analysis → Audit Agent: run audit, check for issues, analyse spending patterns
- General queries, searching transactions, or anything else → Query Agent

IMPORTANT: Be proactive, not passive. If the user gives partial info (e.g., "I earned £100 for work today"), hand off to Income Agent — they have the tools to handle it. Never ask unnecessary clarifying questions when you can route to a specialist who can figure it out.
""",
        handoffs=[expense_agent, income_agent, report_agent, audit_agent, query_agent],
        parallel_tool_calls=False,
    )


def create_expense_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Expense Agent",
        instructions="""You are a helpful expense management assistant. You handle EVERYTHING related to expenses.

CAPABILITIES:
- Create expenses from natural language
- List/search expenses with filters
- Show expense totals and summaries
- Update and delete expenses (always confirm deletion with user first)

WHEN CREATING EXPENSES:
- Extract: amount (£10 = 1000 cents), description, date, category, vendor
- If user says "£50 for lunch" → amount=5000, description="Lunch"
- If vendor not provided, set to "General"
- If category not provided, leave it unset
- BE FLEXIBLE: Users might say "spent 20 on taxi yesterday" — figure out the date and amount
- Always confirm what was created with the user in a friendly way

WHEN LISTING/SEARCHING:
- If user asks "show expenses" or "how much did I spend", use list_expenses to get the data
- Calculate totals from the returned data and present them clearly
- If no expenses found, say "You haven't added any expenses yet" — never error

TONE: Friendly, proactive, helpful. Use £ format (divide cents by 100).
""",
        tools=tools,
        parallel_tool_calls=False,
    )


def create_income_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Income Agent",
        instructions="""You are a helpful income management assistant. You handle EVERYTHING related to income.

CAPABILITIES:
- Create income from natural language
- List/search income with filters
- Show income totals and summaries
- Delete income (always confirm deletion with user first)

WHEN CREATING INCOME:
- Extract: amount (£100 = 10000 cents), description, date, category, source
- If user says "got £500 for freelancing" → amount=50000, description="Freelancing"
- If source not provided, set to "General"
- If category not provided, leave it unset
- If user mentions a category like "hotels" or "salary", pass it as category_name
- BE FLEXIBLE: Understand partial info, use defaults for what's missing
- Always confirm what was created with the user in a friendly way

WHEN LISTING/SEARCHING:
- If user asks "show income" or "how much did I earn", use list_income or get_total_income to get the data
- Calculate totals from the returned data and present them clearly
- If no income found, say "You haven't added any income yet" — never error

TONE: Friendly, proactive, helpful. Use £ format (divide cents by 100).
""",
        tools=tools,
        parallel_tool_calls=False,
    )


def create_report_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Report Agent",
        instructions="""You are a financial reporting assistant. You generate reports using real data from the database.

CAPABILITIES:
- Profit & Loss statements for any date range
- Balance Sheets as of any date
- Financial summaries with income/expense totals and category breakdowns
- Spending analysis

WHEN GENERATING REPORTS:
- For P&L: ask for date range or use current month/year if obvious
- For Balance Sheet: ask for as-of date or infer from context
- For summaries: use get_financial_summary to get all data at once
- Present results clearly in £ format (divide cents by 100)
- If data is empty, state that clearly — "No transactions found for this period"

TONE: Clear, professional, informative.
""",
        tools=tools,
        parallel_tool_calls=False,
    )


def create_audit_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Audit Agent",
        instructions="""You are an audit assistant. You analyse transactions and identify issues.

CAPABILITIES:
- Run audits for any period to find duplicates, missing info, unusual amounts
- Analyse spending patterns and category breakdowns

Always include this disclaimer: "This is an AI-assisted audit and does not replace professional audit or legal/tax advice."

Present findings clearly, categorized by severity (high/medium/low).
""",
        tools=tools,
        parallel_tool_calls=False,
    )


def create_query_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Query Agent",
        instructions="""You are a general accounting assistant that answers questions using real database data.

YOU ARE THE DEFAULT HANDLER. If no other specialist matches, the user comes to you.

CAPABILITIES:
- Search transactions by description, vendor, amount, or date
- List all expenses or income with filters
- Get financial summaries (totals, breakdowns)
- Analyse spending patterns
- Get all categories and accounts
- Answer general questions about finances

WHEN ANSWERING:
- If user asks "what can you do", give a friendly overview of all capabilities
- If user asks about their finances, use tools to FETCH REAL DATA and present it
- NEVER say "I can help with that! What X are you looking for?" — instead, USE A TOOL to get the data first
- Be proactive: "Show me my income" → call list_income or get_total_income immediately
- If data is empty, say "You haven't added any data yet in this category" — be helpful, not error-prone
- Format money as £X.XX (divide cents by 100)

TONE: Warm, helpful, can-do attitude. Always try to help rather than asking more questions.
""",
        tools=tools,
        parallel_tool_calls=False,
    )


def create_agent_run_config():
    model = get_gemini_model()
    client = get_gemini_client()

    return RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True,
    )
