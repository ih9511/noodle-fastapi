import asyncio
import json
import queue

from conditional_custom_executor_multiple_user_test.repository.conditional_custom_executor_multiple_user_test_repository import \
    ConditionalCustomExecutorMultipleUserTestRepository
from template.include.socket_server.utility.color_print import ColorPrinter


class ConditionalCustomExecutorMultipleUserTestRepositoryImpl(ConditionalCustomExecutorMultipleUserTestRepository):
    async def checkTestPointIdle(self, userDefinedReceiverFastAPIChannel, userToken):
        temporaryQueueList = []
        userTokenFound = False

        loop = asyncio.get_event_loop()

        try:
            while True:
                receivedResponseFromSocketClient = await loop.run_in_executor(
                    None, userDefinedReceiverFastAPIChannel.get, False
                )
                data = json.loads(receivedResponseFromSocketClient)

                if data.get("userToken") == userToken:
                    userTokenFound = True
                    break

                temporaryQueueList.append(receivedResponseFromSocketClient)

        except queue.Empty:
            ColorPrinter.print_important_message("아직 데이터를 처리 중이거나 요청한 데이터가 없습니다")
            return userTokenFound

        for item in temporaryQueueList:
            await loop.run_in_executor(None, userDefinedReceiverFastAPIChannel.put, item)

        return userTokenFound

