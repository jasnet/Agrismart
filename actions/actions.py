import os
import time
import logging
from openai import OpenAI
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY_LOCAL")
if not OPENAI_KEY:
    logger.error("OPENAI_API_KEY not set in environment")

client = OpenAI(api_key=OPENAI_KEY)

def call_openai_with_retry(model: str, user_input: str, max_attempts: int = 3, backoff: float = 1.5):
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.responses.create(
                model=model,
                input=user_input,
                # optionally set temperature, max tokens, etc.
            )
            # `output_text` works for simple uses; otherwise inspect resp.output
            text = getattr(resp, "output_text", None)
            if not text:
                # fallback to the structured output if available
                try:
                    outputs = resp.output
                    # collect textual pieces
                    parts = []
                    for item in outputs:
                        for content in item.get("content", []):
                            if content.get("type") == "output_text":
                                parts.append(content.get("text", ""))
                    text = " ".join(parts).strip()
                except Exception:
                    text = None
            return text or ""
        except Exception as e:
            status = getattr(e, "status", None)
            logger.warning("OpenAI call failed (attempt %s/%s): %s", attempt, max_attempts, e)
            if status == 429 or "429" in str(e):
                if attempt < max_attempts:
                    time.sleep(backoff * attempt)
                    continue
            raise

class ActionOpenAIChat(Action):
    def name(self) -> str:
        return "action_openai_chat"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_msg = tracker.latest_message.get("text", "")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        try:
            reply = call_openai_with_retry(model=model, user_input=user_msg)
            if not reply:
                dispatcher.utter_message(text="Sorry, I could not get a response right now.")
            else:
                dispatcher.utter_message(text=reply)
        except Exception as e:
            logger.exception("OpenAI action failed")
            dispatcher.utter_message(text="The service is busy right now. Try again later.")
        return []