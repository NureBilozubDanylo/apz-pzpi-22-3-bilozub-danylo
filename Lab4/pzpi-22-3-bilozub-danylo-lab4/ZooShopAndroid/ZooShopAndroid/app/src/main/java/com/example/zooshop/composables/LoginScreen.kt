package com.example.zooshop.composables

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.zooshop.viewmodel.LoginViewModel
import com.example.zooshop.navigation.Screen

@Composable
fun LoginScreen(navController: NavController, vm: LoginViewModel = viewModel()) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val success by vm.state.collectAsState()

    if (success) {
        navController.navigate(Screen.Shops.route) {
            popUpTo(Screen.Login.route) { inclusive = true }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center
    ) {
        OutlinedTextField(
            value = username,
            onValueChange = { username = it },
            label = { Text("Username") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(12.dp))
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation()
        )
        Spacer(Modifier.height(24.dp))
        Button(
            onClick = { vm.login(username, password) },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Log in")
        }
        Spacer(Modifier.height(8.dp))
        TextButton(onClick = { navController.navigate(Screen.Register.route) }) {
            Text("Create account")
        }
    }
}