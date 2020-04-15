import React, { useState } from "react";
import { View } from "react-native";

import { Menu, Model, Chart } from "../components";
import { SteelFrame } from "../models";
import { fetchData, theme } from "../utils";

export default function SteelFrameScreen() {
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
        setMode(1); // Chart mode
        setModelModeEnabled(false);
      } else {
        setModelModeEnabled(true);
      }
    } catch (error) {
      console.error(error);
    }
    setIsLoading(false);
  }

  function renderVisualisation() {
    if (mode == 0) {
      return (
        <Model
          file={require("../../assets/models/steel-frame.glb")}
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
      );
    } else {
      return <Chart />;
    }
  }

  return (
    <View style={{ flex: 1, flexDirection: "row" }}>
      <View style={{ flex: 5 }}>{renderVisualisation()}</View>
      <Menu
        style={{
          flex: 2,
          borderLeftWidth: 2,
          borderColor: theme.colors.border,
          padding: 10,
          backgroundColor: theme.colors.background,
        }}
        mode={mode}
        setMode={setMode}
        modelModeEnabled={modelModeEnabled}
        isLoading={isLoading}
        refresh={refresh}
      />
    </View>
  );
}
