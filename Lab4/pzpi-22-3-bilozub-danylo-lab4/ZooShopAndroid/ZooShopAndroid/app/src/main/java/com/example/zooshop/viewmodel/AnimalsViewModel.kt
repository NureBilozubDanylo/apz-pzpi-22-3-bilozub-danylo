package com.example.zooshop.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.zooshop.model.Animal
import com.example.zooshop.model.AnimalCreate
import com.example.zooshop.repository.AnimalRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AnimalsViewModel @Inject constructor(
    private val repo: AnimalRepository
): ViewModel() {

    private val _state = MutableStateFlow<List<Animal>>(emptyList())
    val state: StateFlow<List<Animal>> = _state

    private var currentShop: Int? = null

    fun load(shopId: Int) {
        currentShop = shopId
        viewModelScope.launch {
            repo.getAnimals(shopId)
                .onSuccess { _state.value = it }
                .onFailure { _state.value = emptyList() }
        }
    }

    fun addAnimal(data: AnimalCreate) {
        val shopId = currentShop ?: return
        viewModelScope.launch {
            repo.createAnimal(data.copy(shop_id = shopId))
                .onSuccess { load(shopId) }
        }
    }
}