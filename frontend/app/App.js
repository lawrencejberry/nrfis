import React, { Suspense } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import { Text, View } from "react-native";
import Model from "./src/Model";
import SteelFrame from "./src/models/SteelFrame";

function BasementScreen() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Basement!</Text>
    </View>
  );
}

function StrongFloorScreen() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Strong Floor!</Text>
    </View>
  );
}

function SteelFrameScreen() {
  return (
    <Model file={require("./assets/models/steel-frame.glb")}>
      {({ localUri, rotation }) => (
        <SteelFrame localUri={localUri} rotation={rotation} />
      )}
    </Model>
  );
}

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Basement" component={BasementScreen} />
        <Tab.Screen name="Strong Floor" component={StrongFloorScreen} />
        <Tab.Screen name="Steel Frame" component={SteelFrameScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
