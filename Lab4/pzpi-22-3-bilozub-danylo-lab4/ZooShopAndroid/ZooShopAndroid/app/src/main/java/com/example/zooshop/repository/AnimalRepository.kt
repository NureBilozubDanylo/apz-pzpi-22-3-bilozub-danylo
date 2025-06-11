package com.example.zooshop.repository

import com.example.zooshop.model.*
import com.example.zooshop.network.ApiService
import javax.inject.Inject

class AnimalRepository @Inject constructor(private val api: ApiService) {

    suspend fun getAnimals(shopId: Int) = runCatching { api.getAnimals(shopId) }

    suspend fun createAnimal(req: AnimalCreate) = runCatching { api.createAnimal(req) }
}