from dataclasses import dataclass

@dataclass(frozen=True)
class RouteDecision:
    provider: str
    reason: str

class AIRouter:
    providers = ("Auto", "Local", "OpenAI", "Gemini", "Claude", "Qwen", "HuggingFace")

    def choose(self, requested: str, internet_allowed: bool, privacy_first: bool = False) -> RouteDecision:
        if requested == "Local" or privacy_first or not internet_allowed:
            return RouteDecision("Local", "Local route selected for privacy or offline operation.")
        if requested in self.providers and requested != "Auto":
            return RouteDecision(requested, f"Explicit provider selected: {requested}.")
        return RouteDecision("Gemini", "Auto route currently defaults to Gemini until provider scoring is configured.")
