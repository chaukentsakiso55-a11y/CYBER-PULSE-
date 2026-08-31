package com.cyberpulse.infinityos.data

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

class FirebaseRepository(private val auth: FirebaseAuth = FirebaseAuth.getInstance(), private val db: FirebaseFirestore = FirebaseFirestore.getInstance()) {
    fun ensureSignedIn(onResult: (Result<String>) -> Unit) {
        val current = auth.currentUser
        if (current != null) { onResult(Result.success(current.uid)); return }
        auth.signInAnonymously().addOnCompleteListener { task ->
            if (task.isSuccessful) onResult(Result.success(auth.currentUser?.uid.orEmpty())) else onResult(Result.failure(task.exception ?: IllegalStateException("Firebase authentication failed")))
        }
    }
    fun syncDevice(uid: String, deviceId: String, workspace: String, onResult: (Result<Unit>) -> Unit) {
        val payload = mapOf("deviceId" to deviceId, "workspace" to workspace, "platform" to "android", "updatedAt" to System.currentTimeMillis())
        db.collection("users").document(uid).collection("devices").document(deviceId).set(payload).addOnSuccessListener { onResult(Result.success(Unit)) }.addOnFailureListener { onResult(Result.failure(it)) }
    }
}
