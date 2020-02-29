import React from "react";
import { View, Image } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Canvas } from "react-three-fiber";
import { ThemeProvider, Header } from "react-native-elements";

import Model from "./src/Model";
import Menu from "./src/Menu";
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
    <View style={{ flex: 1, flexDirection: "row" }}>
      <Model
        file={require("./assets/models/steel-frame.glb")}
        styles={{ flex: 1 }}
      >
        {({ localUri, rotation }) => (
          <SteelFrame localUri={localUri} rotation={rotation} />
        )}
      </Model>
      <Menu styles={{ flex: 10 }} />
    </View>
  );
}

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <ThemeProvider>
      <Header
        containerStyle={{
          height: 80,
          paddingBottom: 5,
          paddingLeft: 20,
          paddingRight: 20
        }}
        placement="left"
        barStyle="light-content"
        backgroundColor="#404040"
        leftComponent={
          <Image
            source={require("./assets/images/logo.png")}
            style={{ width: 75, height: 55 }}
          />
        }
        centerComponent={
          <Image
            source={require("./assets/images/title.png")}
            style={{ width: 60, height: 10 }}
          />
        }
        rightComponent={
          <Image
            source={require("./assets/images/cambridge.png")}
            style={{ width: 100, height: 20 }}
          />
        }
      />
      <NavigationContainer>
        <Tab.Navigator>
          <Tab.Screen name="Basement" component={BasementScreen} />
          <Tab.Screen name="Strong Floor" component={StrongFloorScreen} />
          <Tab.Screen name="Steel Frame" component={SteelFrameScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}
