package com.cyberpulse.infinityos.ui

import android.provider.Settings
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.cyberpulse.infinityos.core.AIRouter
import com.cyberpulse.infinityos.data.FirebaseRepository

@Composable
fun InfinityApp() {
    val context = LocalContext.current
    val router = remember { AIRouter() }
    val firebase = remember { FirebaseRepository() }
    val deviceId = remember { Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID) ?: "android-device" }
    var workspace by remember { mutableStateOf("Infinity OS") }
    var provider by remember { mutableStateOf("Auto") }
    var command by remember { mutableStateOf("") }
    var status by remember { mutableStateOf("Infinity Core ready") }
    MaterialTheme(colorScheme = darkColorScheme()) {
        Surface(modifier = Modifier.fillMaxSize()) {
            LazyColumn(modifier = Modifier.fillMaxSize().padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("INFINITY OS", style = MaterialTheme.typography.headlineMedium)
                            Text("V7 · NEXUS")
                        }
                        Text(status, style = MaterialTheme.typography.labelMedium)
                    }
                }
                item {
                    OutlinedTextField(value = command, onValueChange = { command = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Ask AEGIS or search Infinity OS") }, trailingIcon = {
                        TextButton(onClick = { val decision = router.choose(provider, true); status = "${decision.provider}: ${command.take(32)}" }) { Text("GO") }
                    })
                }
                item {
                    ElevatedCard(shape = RoundedCornerShape(24.dp)) {
                        Column(Modifier.fillMaxWidth().padding(18.dp)) {
                            Text("Infinity Core", style = MaterialTheme.typography.titleLarge)
                            Text("AI routing · memory · permissions · Firebase sync · AEGIS agents")
                            Spacer(Modifier.height(8.dp))
                            Text("Device: $deviceId", style = MaterialTheme.typography.labelSmall)
                        }
                    }
                }
                item { SelectorCard("Project Memory", listOf("Personal", "School", "Cyber Pulse", "Coding", "StudyLock", "Infinity OS"), workspace) { workspace = it } }
                item { SelectorCard("AI Router", router.providers, provider) { provider = it } }
                item {
                    ElevatedCard(shape = RoundedCornerShape(24.dp)) {
                        Column(Modifier.fillMaxWidth().padding(18.dp)) {
                            Text("Permission Engine", style = MaterialTheme.typography.titleLarge)
                            Text("Files: ASK · Internet: ALLOW · Notifications: ASK · Microphone: ASK · Camera: ASK · Commands: ASK")
                        }
                    }
                }
                item {
                    Button(onClick = {
                        status = "Connecting Firebase…"
                        firebase.ensureSignedIn { authResult ->
                            authResult.onSuccess { uid ->
                                firebase.syncDevice(uid, deviceId, workspace) { syncResult -> status = if (syncResult.isSuccess) "Firebase sync complete" else "Firebase sync failed" }
                            }.onFailure { status = "Firebase auth failed" }
                        }
                    }, modifier = Modifier.fillMaxWidth()) { Text("Sync with Infinity Mesh") }
                }
                item { Text("AEGIS actions are confirmation-gated. This foundation does not run unrestricted device commands.") }
            }
        }
    }
}

@Composable
private fun SelectorCard(title: String, options: List<String>, selected: String, onSelected: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    ElevatedCard(shape = RoundedCornerShape(24.dp)) {
        Column(Modifier.fillMaxWidth().padding(18.dp)) {
            Text(title, style = MaterialTheme.typography.titleLarge)
            Spacer(Modifier.height(10.dp))
            Box {
                OutlinedButton(onClick = { expanded = true }) { Text(selected) }
                DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                    options.forEach { option ->
                        DropdownMenuItem(text = { Text(option) }, onClick = { onSelected(option); expanded = false })
                    }
                }
            }
        }
    }
}
