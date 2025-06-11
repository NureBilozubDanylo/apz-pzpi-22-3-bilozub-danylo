package com.example.zooshop.composables

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.zooshop.model.AnimalCreate
import com.example.zooshop.viewmodel.AnimalsViewModel

@Composable
fun AnimalsScreen(
    navController: NavController,
    shopId: Int,
    vm: AnimalsViewModel = viewModel()
) {
    LaunchedEffect(shopId) { vm.load(shopId) }
    val animals by vm.state.collectAsState()

    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        AddAnimalDialog(
            onDismiss = { showDialog = false },
            onSave = { name, species, breed, age, sex ->
                vm.addAnimal(AnimalCreate(name, species, breed, age, sex))
                showDialog = false
            }
        )
    }

    Scaffold(
        topBar = {
            SmallTopAppBar(
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                title = { Text("Animals") }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { showDialog = true }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) { inner ->
        if (animals.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(inner),
                contentAlignment = Alignment.Center
            ) {
                Text("No animals yet")
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(inner)
            ) {
                items(animals) { a ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                    ) {
                        Column(Modifier.padding(16.dp)) {
                            Text(a.name, style = MaterialTheme.typography.titleMedium)
                            Text("${'$'}{a.species} • ${'$'}{a.breed ?: ""}")
                            Text("Age: ${'$'}{a.age ?: "?"}, Sex: ${'$'}{a.sex ?: "?"}")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun AddAnimalDialog(
    onDismiss: () -> Unit,
    onSave: (String, String, String?, Int?, String?) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var species by remember { mutableStateOf("") }
    var breed by remember { mutableStateOf("") }
    var age by remember { mutableStateOf("") }
    var sex by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            TextButton(onClick = {
                onSave(name, species, breed.takeIf { it.isNotBlank() }, age.toIntOrNull(), sex.takeIf { it.isNotBlank() })
            }) { Text("Save") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } },
        title = { Text("Add animal") },
        text = {
            Column {
                OutlinedTextField(name, { name = it }, label = { Text("Name") })
                OutlinedTextField(species, { species = it }, label = { Text("Species") })
                OutlinedTextField(breed, { breed = it }, label = { Text("Breed") })
                OutlinedTextField(age, { age = it }, label = { Text("Age") })
                OutlinedTextField(sex, { sex = it }, label = { Text("Sex") })
            }
        }
    )
}