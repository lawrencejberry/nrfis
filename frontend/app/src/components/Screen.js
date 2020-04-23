import React, { useState, useContext, useEffect } from "react";
import { View } from "react-native";

import Menu from "./Menu";
import Model from "./Model";
import Chart from "./Chart";
import {
  fetchData,
  fetchTemperatureData,
  theme,
  chartColours,
  modelColourScale,
  LiveStatusContext,
} from "../utils";

export default function Screen(props) {
  const [data, setData] = useState([]);
  const [mode, setMode] = useState(0); // 0 for Model, 1 for Chart
  const [live, setLive] = useState(false);
  const [liveData, setLiveData] = useState([]);
  const [liveMode, setLiveMode] = useState(false); // true for Live, false for Historical
  const [dataRange, setDataRange] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [screenState, setScreenState] = useState({
    dataType: "",
    liveDataType: "str",
    averagingWindow: "",
    startTime: "",
    endTime: "",
  });
  const [chartOptions, setChartOptions] = useState({
    sensors: [], // [{ name: sensorName, isSelected: true}, ... }]
    showTemperature: false,
    temperatureData: [], // [{temperature: x, timestamp: x}, ...]
  });
  const [modelOptions, setModelOptions] = useState({
    showContext: true,
    colourMode: 0, // 0 = adaptive
    scale: [0, 0],
  });

  const liveStatus = useContext(LiveStatusContext);

  useEffect(() => {
    const live = liveStatus.packages.includes(props.packageServerName);
    setLive(live);
    if (liveMode) {
      // Set to absolute colour scale and showTemperature false when pacakge is in live mode
      setModelOptions({
        ...modelOptions,
        colourMode: 1,
        scale: modelColourScale[screenState.liveDataType],
      });
      setChartOptions({ ...chartOptions, showTemperature: false });
      if (screenState.liveDataType === "raw") {
        // Set to chart mode when liveDataType is raw
        setMode(1);
      }
    }
    if (!live) {
      // Set to historical mode when package is not live
      setLiveMode(false);
    }
  }, [liveStatus, screenState.liveDataType, props.packageServerName]);

  useEffect(() => {
    if (liveMode) {
      let ws = new WebSocket(
        `ws://129.169.72.175/fbg/live-data/?data-type=${screenState.liveDataType}`
      );
      ws.onmessage = (event) => {
        const message = event.data;
        const data = JSON.parse(message);
        const newSample = data[props.packageServerName];
        const { timestamp, ...readings } = newSample;
        const sensorNames = Object.keys(readings);
        setChartOptions({
          ...chartOptions,
          showTemperature: false,
          sensors: sensorNames.map((sensorName, index) => ({
            name: sensorName,
            isSelected: index < 3, // By default display only the first three sensors on the chart
            colour: chartColours[index % chartColours.length],
          })),
        });
        setLiveData((liveData) =>
          liveData.length > 30 ? [newSample] : [...liveData, newSample]
        );
      };
      return () => {
        ws.close(); // Clean up the previous websocket when changing the liveMode or dataType
        setLiveData((liveData) => []);
      };
    }
  }, [liveMode, screenState.liveDataType, props.packageServerName]);

  async function refresh(dataType, averagingWindow, startTime, endTime) {
    setIsLoading(true);
    try {
      // Fetch sensor data
      const data = await fetchData(
        props.packageURL,
        dataType,
        averagingWindow,
        startTime.toISOString(),
        endTime.toISOString()
      );
      setData(data);
      const allReadings = data.reduce(
        (acc, { timestamp, ...readings }) =>
          acc.concat(Object.values(readings)),
        []
      );
      const dataRange = [Math.min(...allReadings), Math.max(...allReadings)];
      setDataRange(dataRange);

      // Switch to chart mode if using raw data type
      if (dataType === "raw") {
        setMode(1); // Chart mode
      }
      // Set new screen state
      setScreenState({
        ...screenState,
        dataType: dataType,
        averagingWindow: averagingWindow,
        startTime: startTime,
        endTime: endTime,
      });

      // Set chart options
      const { timestamp, ...readings } = data[0]; // Extract sensor readings for the first sample
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

      // Set model options
      setModelOptions({
        ...modelOptions,
        scale: modelOptions.colourMode ? modelColourScale[dataType] : dataRange,
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
          data={data}
          liveMode={liveMode}
          liveData={liveData}
          modelOptions={modelOptions}
        >
          {({ rotation, zoom, sensorColours }) =>
            props.children({
              rotation,
              zoom,
              sensorColours,
              showContext: modelOptions.showContext,
            })
          }
        </Model>
      );
    } else {
      // Chart
      return (
        <Chart
          data={data}
          liveMode={liveMode}
          liveData={liveData}
          chartOptions={chartOptions}
        />
      );
    }
  }

  return (
    <View style={{ flex: 1, flexDirection: "row" }}>
      <View style={{ flex: 3 }}>{renderVisualisation()}</View>
      <Menu
        style={{
          width: 100,
          borderLeftWidth: 2,
          borderColor: theme.colors.border,
          padding: 10,
          backgroundColor: theme.colors.background,
        }}
        mode={mode}
        setMode={setMode}
        live={live}
        liveMode={liveMode}
        setLiveMode={setLiveMode}
        screenState={screenState}
        setScreenState={setScreenState}
        dataRange={dataRange}
        isLoading={isLoading}
        refresh={refresh}
        chartOptions={chartOptions}
        setChartOptions={setChartOptions}
        modelOptions={modelOptions}
        setModelOptions={setModelOptions}
      />
    </View>
  );
}
