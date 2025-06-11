package com.example.zooshop.repository

import com.example.zooshop.model.*
import com.example.zooshop.network.RetrofitInstance

object ZooRepository {
    private val api = RetrofitInstance.api

    suspend fun login(username: String, password: String) =
        api.login(LoginRequest(username, password))

    suspend fun register(username: String, email: String, password: String) =
        api.register(RegisterRequest(username, email, password))

    suspend fun getShops() = api.getShops()

    suspend fun getAnimals(shopId: Int) = api.getAnimals(shopId)

    
suspend fun getClimateSettings(shopId: Int) = api.getClimateSettingsShop(shopId)
suspend fun getDailyClimateHistory(shopId: Int, date: String) =
    api.getClimate_history_shop_shopid_daily(shopId) // adjust with @Query later

}