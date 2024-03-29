import React, { useState, useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { ThemeProvider } from "react-native-elements";

import {
  BasementScreen,
  StrongFloorScreen,
  SteelFrameScreen,
} from "./src/screens";
import { Header } from "./src/components";
import { theme, LiveStatusContext, fetchLiveStatus } from "./src/utils";

const Tab = createBottomTabNavigator();

export default function App() {
  const [liveStatus, setLiveStatus] = useState({
    live: false,
    packages: [],
    sampling_rate: 0,
  });

  async function checkLiveStatus() {
    try {
      const newLiveStatus = await fetchLiveStatus();
      setLiveStatus(newLiveStatus);
    } catch (error) {
      setLiveStatus({ live: false, packages: [], sampling_rate: 0 });
    }
  }

  useEffect(() => {
    checkLiveStatus();
    const intervalID = setInterval(checkLiveStatus, 5000);
    return () => {
      clearInterval(intervalID);
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <LiveStatusContext.Provider value={liveStatus}>
        <Header />
        <NavigationContainer>
          <Tab.Navigator
            tabBarOptions={{
              activeTintColor: theme.colors.actionable,
            }}
          >
            <Tab.Screen name="Steel Frame" component={SteelFrameScreen} />
            <Tab.Screen name="Basement" component={BasementScreen} />
            <Tab.Screen name="Strong Floor" component={StrongFloorScreen} />
          </Tab.Navigator>
        </NavigationContainer>
      </LiveStatusContext.Provider>
    </ThemeProvider>
  );
}
