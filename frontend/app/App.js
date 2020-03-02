import React, { useState } from "react";
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

async function fetchData(
  sensorPackage,
  dataType,
  averagingWindow,
  startTime,
  endTime
) {
  try {
    const response = await fetch(
      `http://172.21.170.253/fbg/${sensorPackage}/${dataType}/?averaging-window=${averagingWindow}&start-time=${startTime}&end-time=${endTime}`,
      {
        method: "GET",
        headers: { "media-type": "application/json" }
      }
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}

function SteelFrameScreen() {
  const [data, setData] = useState([]);
  const [mode, setMode] = useState(0);
  const [modelModeEnabled, setModelModeEnabled] = useState(true);
  const [dataType, setDataType] = useState("str");
  const [isLoading, setIsLoading] = useState(false);

  async function refresh(dataType, averagingWindow, startTime, endTime) {
    setIsLoading(true);
    // Try fetching data
    try {
      setData(
        await fetchData(
          "steel-frame",
          dataType,
          averagingWindow,
          startTime.toISOString(),
          endTime.toISOString()
        )
      );
      // Set the type of the fetched data
      setDataType(dataType);
      // Enable/disable the model mode button
      if (dataType == "raw") {
        setMode(1);
        setModelModeEnabled(false);
      } else {
        setModelModeEnabled(true);
      }
    } catch (error) {
      console.error(error);
    }
    setIsLoading(false);
  }

  return (
    <View style={{ flex: 1, flexDirection: "row" }}>
      <Model
        file={require("./assets/models/steel-frame.glb")}
        data={data}
        dataType={dataType}
      >
        {({ localUri, rotation, sensorColours }) => (
          <SteelFrame
            localUri={localUri}
            rotation={rotation}
            sensorColours={sensorColours}
          />
        )}
      </Model>
      <Menu
        mode={mode}
        setMode={setMode}
        modelModeEnabled={modelModeEnabled}
        isLoading={isLoading}
        refresh={refresh}
      />
    </View>
  );
}

const Tab = createBottomTabNavigator();

const theme = {
  Text: { style: { fontSize: 20, fontFamily: "Helvetica" } },
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
      <Header
        containerStyle={{
          height: 80,
          paddingBottom: 5,
          paddingLeft: 20,
          paddingRight: 20,
          borderBottomColor: "#404040"
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
