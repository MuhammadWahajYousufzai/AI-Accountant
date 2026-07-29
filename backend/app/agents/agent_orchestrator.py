import json

from agents import Runner

from app.agents.agent_factory import (
    AgentContext,
    create_triage_agent,
    create_expense_agent,
    create_income_agent,
    create_report_agent,
    create_audit_agent,
    create_query_agent,
    create_agent_run_config,
)
from app.tools.expense_tools import (
    create_expense_tool,
    list_expenses_tool,
    get_expense_tool,
    update_expense_tool,
    delete_expense_tool,
)
from app.tools.income_tools import create_income_tool, list_income_tool, delete_income_tool
from app.tools.report_tools import (
    generate_profit_loss_tool,
    generate_balance_sheet_tool,
    get_financial_summary_tool,
)
from app.tools.audit_tools import run_monthly_audit_tool, analyse_spending_tool
from app.tools.transaction_tools import search_transactions_tool
from app.tools.utility_tools import (
    get_all_categories_tool,
    get_all_accounts_tool,
    get_total_income_tool,
    get_total_expense_tool,
)


def _build_agents(get_db, get_user_id):
    expense_tools = [
        create_expense_tool(get_db, get_user_id),
        list_expenses_tool(get_db, get_user_id),
        get_expense_tool(get_db, get_user_id),
        update_expense_tool(get_db, get_user_id),
        delete_expense_tool(get_db, get_user_id),
    ]
    income_tools = [
        create_income_tool(get_db, get_user_id),
        list_income_tool(get_db, get_user_id),
        delete_income_tool(get_db, get_user_id),
        get_total_income_tool(get_db, get_user_id),
    ]
    report_tools = [
        generate_profit_loss_tool(get_db, get_user_id),
        generate_balance_sheet_tool(get_db, get_user_id),
        get_financial_summary_tool(get_db, get_user_id),
    ]
    audit_tools = [
        run_monthly_audit_tool(get_db, get_user_id),
        analyse_spending_tool(get_db, get_user_id),
    ]
    query_tools = [
        search_transactions_tool(get_db, get_user_id),
        list_expenses_tool(get_db, get_user_id),
        list_income_tool(get_db, get_user_id),
        get_financial_summary_tool(get_db, get_user_id),
        analyse_spending_tool(get_db, get_user_id),
        get_all_categories_tool(get_db, get_user_id),
        get_all_accounts_tool(get_db, get_user_id),
        get_total_income_tool(get_db, get_user_id),
        get_total_expense_tool(get_db, get_user_id),
    ]

    return {
        "triage": create_triage_agent(
            create_expense_agent(expense_tools),
            create_income_agent(income_tools),
            create_report_agent(report_tools),
            create_audit_agent(audit_tools),
            create_query_agent(query_tools),
        ),
    }


async def process_message(
    user_id: str,
    conversation_id: str,
    message: str,
    db_factory,
):
    current_user_id = user_id

    def get_db():
        return db_factory()

    def get_uid():
        return current_user_id

    agents = _build_agents(get_db, get_uid)
    triage_agent = agents["triage"]
    run_config = create_agent_run_config()

    context = AgentContext(user_id=user_id, db_session_factory=db_factory)

    result = await Runner.run(
        triage_agent,
        input=message,
        context=context,
        max_turns=30,
        run_config=run_config,
    )

    tool_calls_info = []
    actions = []

    for item in result.new_items:
        if item.type == "tool_call_item":
            tool_name = item.tool_name or "unknown"
            raw_args = item.raw_item.arguments if hasattr(item.raw_item, "arguments") else "{}"
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {}
            else:
                args = raw_args
            tool_calls_info.append({
                "tool": tool_name,
                "args": args,
            })
            actions.append({
                "type": tool_name,
                "status": "success",
                "details": args,
            })

    return {
        "response": result.final_output,
        "tool_calls": tool_calls_info,
        "tool_results": tool_calls_info,
        "actions": actions,
    }
