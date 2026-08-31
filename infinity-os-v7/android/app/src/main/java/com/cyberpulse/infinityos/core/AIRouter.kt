package com.cyberpulse.infinityos.core

class AIRouter {
    val providers = listOf("Auto", "Local", "OpenAI", "Gemini", "Claude", "Qwen", "HuggingFace")
    fun choose(requested: String, internetAllowed: Boolean, privacyFirst: Boolean = false): RouteDecision {
        if (requested == "Local" || privacyFirst || !internetAllowed) return RouteDecision("Local", "Local route selected for privacy or offline operation.")
        if (requested != "Auto" && requested in providers) return RouteDecision(requested, "Explicit provider selected.")
        return RouteDecision("Gemini", "Auto route defaults to Gemini until provider scoring is configured.")
    }
}
