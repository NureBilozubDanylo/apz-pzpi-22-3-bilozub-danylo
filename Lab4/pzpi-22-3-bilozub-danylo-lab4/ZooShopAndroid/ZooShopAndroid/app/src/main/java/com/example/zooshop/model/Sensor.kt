package com.example.zooshop.model
data class Sensor(
    val sensor_id: Int,
    val type: String,
    val location: String,
    val current_value: Float,
    val last_maintenance: String,
    val sensor_link: String?
)
data class SensorCreate(
    val shop_id: Int,
    val type: String,
    val location: String,
    val sensor_link: String? = null
)