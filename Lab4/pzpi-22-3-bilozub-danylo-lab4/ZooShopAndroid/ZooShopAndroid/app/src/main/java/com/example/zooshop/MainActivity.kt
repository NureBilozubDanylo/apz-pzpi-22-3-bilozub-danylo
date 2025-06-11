package com.example.zooshop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import dagger.hilt.android.AndroidEntryPoint
import com.example.zooshop.navigation.ZooNavGraph
import com.example.zooshop.ui.theme.ZooShopTheme

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ZooShopTheme {
                Surface(color = MaterialTheme.colorScheme.background) {
                    ZooNavGraph()
                }
            }
        }
    }
}