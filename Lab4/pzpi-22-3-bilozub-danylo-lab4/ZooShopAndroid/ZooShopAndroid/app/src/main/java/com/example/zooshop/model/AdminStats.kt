package com.example.zooshop.model
data class AdminStats(
    val uptime_sec: Long,
    val cpu_percent: Float,
    val ram_used_mb: Float,
    val ram_total_mb: Float,
    val disk_used_gb: Float,
    val disk_total_gb: Float
)
data class DbStatus(
    val table: String,
    val rows: Int
)