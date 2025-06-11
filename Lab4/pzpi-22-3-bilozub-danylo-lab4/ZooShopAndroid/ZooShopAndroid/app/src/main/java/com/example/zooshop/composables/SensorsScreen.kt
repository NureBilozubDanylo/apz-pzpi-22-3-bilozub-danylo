package com.example.zooshop.composables

import androidx.compose.foundation.clickable
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
import com.example.zooshop.model.Sensor
import com.example.zooshop.viewmodel.SensorsViewModel

@Composable
fun SensorsScreen(
    navController: NavController,
    shopId: Int,
    viewModel: SensorsViewModel = viewModel()
) {
    // Запускаємо завантаження лише один раз для конкретного shopId
    LaunchedEffect(shopId) { viewModel.load(shopId) }

    val sensors by viewModel.state.collectAsState()
    val loading by viewModel.loading.collectAsState()
    val error by viewModel.error.collectAsState()

    var showDialog by remember { mutableStateOf(false) }

    /* ─────── Dialog для створення нового сенсора ─────── */
    if (showDialog) {
        AddSensorDialog(
            onDismiss = { showDialog = false },
            onSave = { name, type ->
                viewModel.addSensor(shopId, name, type)
                showDialog = false
            }
        )
    }

    /* ─────── UI ─────── */
    Scaffold(
        topBar = {
            SmallTopAppBar(
                title = { Text("Sensors") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { showDialog = true }) {
                Icon(Icons.Default.Add, contentDescription = "Add sensor")
            }
        }
    ) { innerPadding ->
        when {
            loading -> {
                /* Лоудер */
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }

            error != null -> {
                /* Повідомлення про помилку */
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Error: $error")
                }
            }

            sensors.isEmpty() -> {
                /* Порожній стан */
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    Text("No sensors yet")
                }
            }

            else -> {
                /* Список сенсорів */
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                ) {
                    items(sensors) { sensor ->
                        SensorCard(
                            sensor = sensor,
                            onClick = {
                                navController.navigate("climate/$shopId/${sensor.id}")
                            }
                        )
                    }
                }
            }
        }
    }
}

/* ──────────────────────────────────────────────────────── */
/* Картка сенсора                                          */
/* ──────────────────────────────────────────────────────── */
@Composable
private fun SensorCard(sensor: Sensor, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp, horizontal = 8.dp)
            .clickable { onClick() },
        shape = MaterialTheme.shapes.medium
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(sensor.name, style = MaterialTheme.typography.titleMedium)
            Text(sensor.type)
        }
    }
}

/* ──────────────────────────────────────────────────────── */
/* Діалог створення сенсора                                */
/* ──────────────────────────────────────────────────────── */
@Composable
private fun AddSensorDialog(
    onDismiss: () -> Unit,
    onSave: (name: String, type: String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var type by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            TextButton(
                onClick = { onSave(name.trim(), type.trim()) },
                enabled = name.isNotBlank() && type.isNotBlank()
            ) { Text("Save") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        },
        title = { Text("Add Sensor") },
        text = {
            Column {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Name") },
                    singleLine = true
                )
                OutlinedTextField(
                    value = type,
                    onValueChange = { type = it },
                    label = { Text("Type") },
                    singleLine = true
                )
            }
        }
    )
}
