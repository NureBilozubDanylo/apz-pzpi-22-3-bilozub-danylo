package com.example.zooshop.repository

import com.example.zooshop.model.*
import com.example.zooshop.network.ApiService
import com.example.zooshop.network.TokenStore
import javax.inject.Inject

class AuthRepository @Inject constructor(
    private val api: ApiService,
    private val tokenStore: TokenStore
) {
    suspend fun login(username: String, password: String) = runCatching {
        val token = api.login(LoginRequest(username, password)).token
        tokenStore.token = token
    }

    suspend fun register(username: String, email: String, password: String) = runCatching {
        val token = api.register(RegisterRequest(username, email, password)).token
        tokenStore.token = token
    }
}