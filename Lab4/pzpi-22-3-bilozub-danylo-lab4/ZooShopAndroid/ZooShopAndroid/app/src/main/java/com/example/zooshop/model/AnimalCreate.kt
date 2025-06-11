package com.example.zooshop.model
data class AnimalCreate(
    val name: String,
    val species: String,
    val breed: String? = null,
    val age: Int? = null,
    val sex: String? = null,
    val weight: Float? = null,
    val shop_id: Int? = null
)