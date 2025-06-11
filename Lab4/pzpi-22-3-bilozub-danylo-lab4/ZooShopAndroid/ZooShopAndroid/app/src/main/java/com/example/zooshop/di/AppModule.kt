package com.example.zooshop.di

import com.example.zooshop.network.*
import com.example.zooshop.repository.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    private const val BASE_URL = "http://127.0.0.1:8000"

    @Provides
    @Singleton
    fun provideTokenStore(): TokenStore = TokenStore()

    @Provides
    @Singleton
    fun provideOkHttp(tokenStore: TokenStore): OkHttpClient =
        OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(tokenStore))
            .build()

    @Provides
    @Singleton
    fun provideRetrofit(client: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService =
        retrofit.create(ApiService::class.java)

    /* -------- repositories -------- */
    @Provides
    @Singleton
    fun provideAuthRepository(api: ApiService, tokenStore: TokenStore): AuthRepository =
        AuthRepository(api, tokenStore)

    @Provides
    @Singleton
    fun provideShopRepository(api: ApiService): ShopRepository = ShopRepository(api)

    @Provides
    @Singleton
    fun provideAnimalRepository(api: ApiService): AnimalRepository = AnimalRepository(api)
}