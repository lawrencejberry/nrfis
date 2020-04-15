import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { ThemeProvider } from "react-native-elements";

import {
  BasementScreen,
  StrongFloorScreen,
  SteelFrameScreen
} from "./src/screens";
import { Header } from "./src/components";
import { theme } from "./src/utils";

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Header />
      <NavigationContainer>
        <Tab.Navigator
          tabBarOptions={{
            activeTintColor: theme.colors.actionable
          }}
        >
          <Tab.Screen name="Basement" component={BasementScreen} />
          <Tab.Screen name="Strong Floor" component={StrongFloorScreen} />
          <Tab.Screen name="Steel Frame" component={SteelFrameScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}
