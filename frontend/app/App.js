import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Canvas } from "react-three-fiber";

import Model from "./src/Model";
import { SteelFrame, LoadingIndicator } from "./src/models";

function BasementScreen() {
  return (
    <Canvas camera={{ position: [0, 0, 50] }}>
      <ambientLight intensity={0.5} />
      <spotLight intensity={0.8} position={[300, 300, 400]} />
      <LoadingIndicator />
    </Canvas>
  );
}

function StrongFloorScreen() {
  return (
    <Canvas camera={{ position: [0, 0, 50] }}>
      <ambientLight intensity={0.5} />
      <spotLight intensity={0.8} position={[300, 300, 400]} />
      <LoadingIndicator />
    </Canvas>
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
