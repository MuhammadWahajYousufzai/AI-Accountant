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
        name="Accounting Triage Agent",
        instructions="""You are the triage agent for an accounting system. Your job is to:

1. Read the user's message
2. Determine their intent
3. Handoff to the appropriate specialist agent

Classification rules:
- If the user wants to CREATE, VIEW, UPDATE, or DELETE expenses -> handoff to Expense Agent
- If the user wants to CREATE, VIEW, UPDATE, or DELETE income -> handoff to Income Agent
- If the user asks for reports, P&L, profit and loss, balance sheet -> handoff to Report Agent
- If the user asks for audit, review, check, anomalies -> handoff to Audit Agent
- If the user asks a general question, wants a summary, or searches transactions -> handoff to Query Agent
- If unsure, ask clarifying questions before handing off

Never refuse to handoff. Always route to the most specific agent.
""",
        handoffs=[expense_agent, income_agent, report_agent, audit_agent, query_agent],
    )


def create_expense_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Expense Management Agent",
        instructions="""You are an expense management agent. You help users manage their business expenses.

When creating an expense:
- Extract: amount, description, date, category name, vendor
- Validate all required fields are present
- Call create_expense tool to save the transaction
- Confirm to the user what was created

When listing/searching expenses: Call list_expenses with appropriate filters
When viewing a specific expense: Call get_expense
When updating: Confirm changes with user, call update_expense
When deleting: ALWAYS ask the user to confirm before deleting. Never delete on ambiguous instructions.

Always use real data from the database via tools. Never fabricate numbers or financial data.
""",
        tools=tools,
    )


def create_income_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Income Management Agent",
        instructions="""You are an income management agent. You help users track their income.

When creating income:
- Extract: amount, description, date, source, category name
- Call create_income tool to save
- Confirm to the user

When listing/searching: Call list_income with appropriate filters
When deleting: ALWAYS confirm with user first.

Always use real data from the database via tools.
""",
        tools=tools,
    )


def create_report_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Financial Report Agent",
        instructions="""You are a financial reporting agent. You generate reports using real database data.

For P&L: Ask for date range or infer from context. Call generate_profit_loss tool.
For Balance Sheet: Ask for as-of date or infer. Call generate_balance_sheet tool.
For financial summary: Call get_financial_summary tool.

Report calculations are done by the backend. You present the results clearly to the user.
Always specify the reporting period and that data comes from the database.
If data is missing, state that clearly.
""",
        tools=tools,
    )


def create_audit_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Monthly Audit Agent",
        instructions="""You are an audit agent. You analyze transactions and identify issues.

Call run_monthly_audit with the period to analyze.
Present findings clearly, categorized by severity.
Always include this disclaimer in your response: "This is an AI-assisted audit and does not replace professional audit or legal/tax advice."

Types of findings to look for:
- Duplicate transactions
- Missing information (description, vendor, category)
- Unusual amounts (statistical outliers)
- Spending pattern anomalies
- Categorization issues
- Date inconsistencies
""",
        tools=tools,
    )


def create_query_agent(tools: list) -> Agent:
    return Agent[AgentContext](
        name="Accounting Query Agent",
        instructions="""You are a general accounting query agent. You answer questions using real database data.

Use search_transactions to find specific transactions by description or vendor.
Use list_expenses and list_income for filtered lists.
Use get_financial_summary for aggregated data.
Use analyse_spending for spending pattern analysis.

If data is missing to answer a question accurately, state that clearly.
Explain financial results in simple, clear language.
Always cite specific amounts and dates from the data.
""",
        tools=tools,
    )


def create_agent_run_config():
    model = get_gemini_model()
    client = get_gemini_client()

    return RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True,
    )
