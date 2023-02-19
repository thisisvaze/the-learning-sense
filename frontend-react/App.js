import * as React from "react";
import { Text, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Home from "./Home.js";
import Lessons from "./Lessons.js";
import Profile from "./Profile.js";
import { Ionicons } from "@expo/vector-icons";

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === "Add Lessons") {
              iconName = focused ? "cube" : "cube-outline";
            } else if (route.name === "Home") {
              iconName = focused ? "home" : "home-outline";
            } else if (route.name === "Profile") {
              iconName = focused ? "school" : "school-outline";
            }

            // You can return any component that you like here!
            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: "primary.500",
          tabBarInactiveTintColor: "gray.500",
          headerShown: false,
        })}
      >
        <Tab.Screen name="Home" component={Home} />
        <Tab.Screen name="Add Lessons" component={Lessons} />
        <Tab.Screen name="Profile" component={Profile} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
