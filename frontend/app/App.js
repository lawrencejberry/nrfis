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

const Tab = createBottomTabNavigator();

const theme = {
  colors: {
    primary: "#737f8a"
  },
  Text: {
    style: {
      fontSize: 20,
      fontFamily: Platform.select({ default: "Roboto", ios: "Helvetica" })
    }
  },
  Divider: { style: { margin: 4 } },
  Button: {
    containerStyle: {
      paddingTop: 5,
      paddingBottom: 5,
      paddingLeft: 10,
      paddingRight: 10
    },
    buttonStyle: { borderWidth: 1 },
    titleStyle: {
      fontSize: 16
    }
  },
  ButtonGroup: { textStyle: { fontSize: 16 } }
};

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Header />
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
