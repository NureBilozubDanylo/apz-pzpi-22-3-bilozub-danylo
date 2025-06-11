package com.example.zooshop.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.NavType
import androidx.navigation.navArgument
import com.example.zooshop.composables.*

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Register : Screen("register")
    object Shops : Screen("shops")
    object Animals : Screen("animals/{shopId}") {
        fun passShopId(shopId: Int) = "animals/$shopId"
    }
}

@Composable
fun ZooNavGraph(
    navController: NavHostController = rememberNavController()
) {
    NavHost(navController = navController, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) { LoginScreen(navController) }
        composable(Screen.Register.route) { RegisterScreen(navController) }
        composable(Screen.Shops.route) { ShopsScreen(navController) }
        composable(
            Screen.Animals.route,
            arguments = listOf(navArgument("shopId") { type = NavType.IntType })
        ) { backStackEntry ->
            val shopId = backStackEntry.arguments?.getInt("shopId") ?: return@composable
            AnimalsScreen(navController, shopId)
        }
    }
}