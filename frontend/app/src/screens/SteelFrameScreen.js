import React, { useState } from "react";
import { View } from "react-native";

import { Menu, Model, Chart } from "../components";
import { SteelFrame } from "../models";
import { fetchData, fetchTemperatureData, theme, chartColours } from "../utils";

export default function SteelFrameScreen() {
  const [data, setData] = useState([]);
  const [mode, setMode] = useState(0); // 0 for Model, 1 for Chart
  const [dataType, setDataType] = useState("str");
  const [isLoading, setIsLoading] = useState(false);
  const [chartOptions, setChartOptions] = useState({
    sensors: [], // [{ name: sensorName, isSelected: true}, ... }]
    showTemperature: false,
    temperatureData: [], // [{temperature: x, timestamp: x}, ...]
  });

  async function refresh(dataType, averagingWindow, startTime, endTime) {
    setIsLoading(true);
    try {
      // Fetch sensor data
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
      }
      // Set all sensors selected and fetch temperature data
      const { timestamp, ...readings } = props.data[0]; // Extract sensor readings for the first sample
      const sensorNames = Object.keys(readings); // Extract the sensor names
      setChartOptions({
        ...chartOptions,
        sensors: sensorNames.map((sensorName, index) => ({
          name: sensorName,
          isSelected: index < 3, // By default display only the first three sensors on the chart
          colour: chartColours[index % chartColours.length],
        })),
        temperatureData: await fetchTemperatureData(startTime, endTime),
      });
    } catch (error) {
      console.error(error);
    }
    setIsLoading(false);
  }

  function renderVisualisation() {
    if (mode == 0) {
      // Model
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
      // Chart
      return <Chart data={data} chartOptions={chartOptions} />;
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
        modelModeEnabled={dataType !== "raw"} // Model mode only enabled for str or tmp
        isLoading={isLoading}
        refresh={refresh}
        chartOptions={chartOptions}
        setChartOptions={setChartOptions}
      />
    </View>
  );
}
