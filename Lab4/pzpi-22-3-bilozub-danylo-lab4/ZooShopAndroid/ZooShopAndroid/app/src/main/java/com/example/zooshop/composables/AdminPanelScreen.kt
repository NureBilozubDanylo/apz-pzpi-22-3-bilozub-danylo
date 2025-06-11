package com.example.zooshop.composables

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.example.zooshop.network.ApiService
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject
import javax.inject.Inject

@HiltViewModel
class AdminPanelViewModel @Inject constructor(
    private val api: ApiService
) : ViewModel() {

    var serverStats by mutableStateOf<List<Pair<String, String>>>(emptyList())
        private set

    var dbEntries by mutableStateOf<List<Pair<String, String>>>(emptyList())
        private set

    var isLoading by mutableStateOf(true)
        private set

    var error by mutableStateOf<String?>(null)
        private set

    init { refresh() }

    fun refresh() {
        viewModelScope.launch {
            isLoading = true
            try {
                val sysJson = JSONObject(api.admin_system_status().string())
                serverStats = listOf(
                    "Uptime" to sysJson.optString("uptime"),
                    "CPU" to "${sysJson.optDouble("cpu", 0.0)}%",
                    "RAM" to "${sysJson.optInt("ramUsed")}/${sysJson.optInt("ramTotal")} MB",
                    "Disk" to "${sysJson.optDouble("diskUsed")}/${sysJson.optDouble("diskTotal")} GB"
                )

                val dbJson = JSONObject(api.admin_db_status().string())
                val tables: JSONArray = dbJson.getJSONArray("tables")
                dbEntries = (0 until tables.length()).map { i ->
                    val t = tables.getJSONObject(i)
                    t.getString("name") to String.format("%.2f", t.getDouble("sizeMb"))
                }
                error = null
            } catch (e: Exception) {
                error = e.localizedMessage
            } finally {
                isLoading = false
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdminPanelScreen(
    navController: NavController,
    viewModel: AdminPanelViewModel = androidx.hilt.navigation.compose.hiltViewModel()
) {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    val serverStats = viewModel.serverStats
    val dbEntries = viewModel.dbEntries
    val isLoading = viewModel.isLoading
    val error = viewModel.error

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                Text(
                    text = "Menu",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(16.dp)
                )
                NavigationDrawerItem(
                    label = { Text("Shops") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate("shops")
                    }
                )
                NavigationDrawerItem(
                    label = { Text("Animals") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate("animals")
                    }
                )
                NavigationDrawerItem(
                    label = { Text("Sensors") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        navController.navigate("sensors")
                    }
                )
            }
        }
    ) {
        Scaffold(
            topBar = {
                SmallTopAppBar(
                    title = {
                        Text(
                            text = "ZooHelper",
                            style = MaterialTheme.typography.titleLarge
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    },
                    actions = {
                        IconButton(onClick = { navController.navigate("notifications") }) {
                            Icon(Icons.Default.Notifications, contentDescription = "Notifications")
                        }
                    }
                )
            }
        ) { innerPadding ->
            when {
                isLoading -> {
                    Box(
                        Modifier
                            .fillMaxSize()
                            .padding(innerPadding),
                        contentAlignment = Alignment.Center
                    ) { CircularProgressIndicator() }
                }
                error != null -> {
                    Box(
                        Modifier
                            .fillMaxSize()
                            .padding(innerPadding),
                        contentAlignment = Alignment.Center
                    ) { Text(error ?: "Unknown error", color = MaterialTheme.colorScheme.error) }
                }
                else -> {
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding)
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                        horizontalAlignment = Alignment.Start
                    ) {
                        // ─────────────── Page title ───────────────
                        item {
                            Text(
                                text = "Admin Panel",
                                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.SemiBold)
                            )
                        }

                        // ─────────────── Server stats card ───────────────
                        if (serverStats.isNotEmpty()) item {
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = MaterialTheme.shapes.medium
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(
                                        text = "Server stats",
                                        style = MaterialTheme.typography.titleSmall,
                                        fontWeight = FontWeight.SemiBold
                                    )
                                    Spacer(modifier = Modifier.height(8.dp))
                                    serverStats.forEach { (label, value) ->
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Text("•")
                                            Spacer(modifier = Modifier.width(6.dp))
                                            Text("$label: $value")
                                        }
                                    }
                                }
                            }
                        }

                        // ─────────────── Database card ───────────────
                        if (dbEntries.isNotEmpty()) item {
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = MaterialTheme.shapes.medium
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(
                                        text = "Database",
                                        style = MaterialTheme.typography.titleSmall,
                                        fontWeight = FontWeight.SemiBold
                                    )
                                    Spacer(modifier = Modifier.height(8.dp))

                                    // Header
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = "Table",
                                            modifier = Modifier.weight(1f),
                                            style = MaterialTheme.typography.labelMedium,
                                            fontWeight = FontWeight.Bold
                                        )
                                        Text(
                                            text = "Size, MB",
                                            style = MaterialTheme.typography.labelMedium,
                                            fontWeight = FontWeight.Bold,
                                            textAlign = TextAlign.End
                                        )
                                    }
                                    Divider()

                                    dbEntries.forEach { (table, size) ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .padding(vertical = 4.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(
                                                text = table,
                                                modifier = Modifier.weight(1f)
                                            )
                                            Text(
                                                text = size,
                                                textAlign = TextAlign.End
                                            )
                                        }
                                        Divider()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}