import asyncio
from pyrit.common import IN_MEMORY, initialize_pyrit
from pyrit.executor.attack import ConsoleAttackResultPrinter, PromptSendingAttack
from pyrit.prompt_target import DatabricksChatTarget


async def run_pyrit_integration_test():
    initialize_pyrit(memory_db_type=IN_MEMORY)

    target = DatabricksChatTarget()

    attack = PromptSendingAttack(objective_target=target)
    result = await attack.execute_async(objective="This is a test prompt")  # type: ignore

    printer = ConsoleAttackResultPrinter()
    await printer.print_conversation_async(result=result)  # type: ignore


def run_pyrit_test():
    asyncio.run(run_pyrit_integration_test())
