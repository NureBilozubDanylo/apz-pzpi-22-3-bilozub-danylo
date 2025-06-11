package com.example.zooshop.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.zooshop.model.Shop
import com.example.zooshop.repository.ShopRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ShopsViewModel @Inject constructor(
    private val repo: ShopRepository
): ViewModel() {

    private val _state = MutableStateFlow<List<Shop>>(emptyList())
    val state: StateFlow<List<Shop>> = _state

    private val _loading = MutableStateFlow(false)
    val loading: StateFlow<Boolean> = _loading

    fun load() {
        viewModelScope.launch {
            _loading.value = true
            repo.getUserShops()
                .onSuccess { _state.value = it }
                .onFailure { /* TODO handle */ }
            _loading.value = false
        }
    }
}