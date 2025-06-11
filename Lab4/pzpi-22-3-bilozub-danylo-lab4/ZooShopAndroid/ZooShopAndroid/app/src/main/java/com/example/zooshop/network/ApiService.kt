package com.example.zooshop.network

import com.example.zooshop.model.*
import retrofit2.http.*

interface ApiService {

    /* -------- Auth -------- */
    @POST("/auth/login")
    suspend fun login(@Body body: LoginRequest): TokenResponse

    @POST("/auth/register")
    suspend fun register(@Body body: RegisterRequest): TokenResponse

    /* -------- Shops -------- */
    @GET("/shops/user")
    suspend fun getUserShops(): List<Shop>

    @GET("/shops/{id}")
    suspend fun getShop(@Path("id") id: Int): Shop

    /* -------- Animals -------- */
    @GET("/animals/shop/{shopId}")
    suspend fun getAnimals(@Path("shopId") shopId: Int): List<Animal>

    @POST("/animals/")
    suspend fun createAnimal(@Body body: AnimalCreate): Animal

    /* -------- Sensors -------- */
    @GET("/sensors/shop/{shopId}")
    suspend fun getSensors(@Path("shopId") shopId: Int): List<Sensor>

    @POST("/sensors/")
    suspend fun createSensor(@Body body: SensorCreate): Sensor

    /* -------- Climate -------- */
    @GET("/climate/shop/{shopId}/history")
    suspend fun getClimateHistory(@Path("shopId") shopId: Int): List<ClimateRecord>

    /* -------- Admin -------- */
    @GET("/admin/stats")
    suspend fun getAdminStats(): AdminStats

    @GET("/admin/db/status")
    suspend fun getDbStatus(): List<DbStatus>
}