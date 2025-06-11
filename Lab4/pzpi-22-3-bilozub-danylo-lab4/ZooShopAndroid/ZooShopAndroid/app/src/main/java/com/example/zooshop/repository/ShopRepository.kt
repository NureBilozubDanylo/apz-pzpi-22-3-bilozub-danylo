package com.example.zooshop.repository

import com.example.zooshop.model.Shop
import com.example.zooshop.network.ApiService
import javax.inject.Inject

class ShopRepository @Inject constructor(private val api: ApiService) {

    suspend fun getUserShops(): Result<List<Shop>> = runCatching { api.getUserShops() }
}