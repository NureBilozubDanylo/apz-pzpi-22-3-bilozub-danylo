package com.example.zooshop.composables

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.zooshop.navigation.Screen
import com.example.zooshop.viewmodel.ShopsViewModel

@Composable
fun ShopsScreen(
    navController: NavController,
    vm: ShopsViewModel = viewModel()
) {
    val shops by vm.state.collectAsState()
    val loading by vm.loading.collectAsState()

    LaunchedEffect(Unit) { vm.load() }

    Scaffold(
        topBar = {
            SmallTopAppBar(title = { Text("My Shops") })
        }
    ) { inner ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(inner),
            contentAlignment = Alignment.Center
        ) {
            when {
                loading -> CircularProgressIndicator()
                shops.isEmpty() -> Text("No shops yet")
                else -> Column(
                    Modifier.fillMaxWidth().padding(16.dp)
                ) {
                    shops.forEach { shop ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 6.dp)
                                .clickable {
                                    navController.navigate(Screen.Animals.passShopId(shop.shop_id))
                                }
                        ) {
                            Column(Modifier.padding(16.dp)) {
                                Text(shop.name, style = MaterialTheme.typography.titleMedium)
                                Text(shop.address)
                                if (!shop.description.isNullOrBlank())
                                    Text(shop.description!!)
                            }
                        }
                    }
                }
            }
        }
    }
}