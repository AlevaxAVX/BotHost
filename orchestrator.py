import asyncio
import os
from datetime import datetime
from typing import Dict, List

class BotOrchestrator:
    """
    Handles the lifecycle of bot processes.
    """
    def __init__(self):
        self.active_processes: Dict[str, asyncio.subprocess.Process] = {}
        self.logs: Dict[str, List[str]] = {}

    async def start_bot(self, bot_id: str, command: List[str], cwd: str):
        if bot_id in self.active_processes:
            return False, "Bot is already running."

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            self.active_processes[bot_id] = process
            self.logs[bot_id] = []
            
            # Start background tasks to read logs
            asyncio.create_task(self._capture_logs(bot_id, process.stdout, "INFO"))
            asyncio.create_task(self._capture_logs(bot_id, process.stderr, "ERROR"))
            
            return True, "Bot started successfully."
        except Exception as e:
            return False, f"Failed to start bot: {str(e)}"

    async def stop_bot(self, bot_id: str):
        process = self.active_processes.get(bot_id)
        if process:
            process.terminate()
            await process.wait()
            del self.active_processes[bot_id]
            return True, "Bot stopped."
        return False, "Bot is not running."

    async def _capture_logs(self, bot_id, stream, level):
        while True:
            line = await stream.readline()
            if not line:
                break
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_msg = f"[{timestamp}] [{level}] {line.decode().strip()}"
            
            if bot_id not in self.logs:
                self.logs[bot_id] = []
            
            self.logs[bot_id].append(log_msg)
            # Keep only the last 500 lines
            if len(self.logs[bot_id]) > 500:
                self.logs[bot_id].pop(0)
