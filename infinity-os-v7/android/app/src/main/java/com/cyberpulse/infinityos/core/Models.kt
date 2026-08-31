package com.cyberpulse.infinityos.core

data class InfinityPermission(val name: String, val mode: PermissionMode)
enum class PermissionMode { ALLOW, ASK, BLOCK }
data class Workspace(val name: String)
data class RouteDecision(val provider: String, val reason: String)
