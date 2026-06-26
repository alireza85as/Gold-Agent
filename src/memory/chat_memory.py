import json
import os
from datetime import datetime


class ChatMemory:
    """ A simple chat memory manager that stores conversation history in a JSON file."""

    def __init__(self, file_path="memory.json"):
        self.file_path = file_path

        # Create an empty JSON file if it doesn't already exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self):
        # Load all chat memories from the JSON file.
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, user_message, assistant_message):
        # Save a new conversation exchange to the memory file.
        memories = self.load()

        new_memory = {
            "user": user_message,
            "assistant": assistant_message,
            "time": datetime.now().isoformat(),
        }

        memories.append(new_memory)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, ensure_ascii=False, indent=4)

    def get_history(self, limit=10):
        # Retrieve the most recent conversation history.
        memories = self.load()

        return memories[-limit:]
