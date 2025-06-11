package com.example.zooshop.model
data class Animal(
    val id: Int,
    val name: String,
    val species: String,
    val breed: String?,
    val age: Int?,
    val sex: String?,
    val weight: Float?
)