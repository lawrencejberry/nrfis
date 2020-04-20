import React, { useState } from "react";
import { View } from "react-native";

import { Menu, Model, Chart } from "../components";
import { SteelFrame } from "../models";
import { fetchData, fetchTemperatureData, theme, chartColours } from "../utils";

export default function SteelFrameScreen() {
  const [data, setData] = useState([
    {
      timestamp: 1586952060000,
      FR_FBG_CL_D1_1a: -46.90169538539861,
      FR_FBG_CL_D1_1b: -76.44770185283656,
      FR_FBG_BM_D13_2a: -117.68629645604933,
    },
    {
      timestamp: 1586952120000,
      FR_FBG_CL_D1_1a: -46.55613225593654,
      FR_FBG_CL_D1_1b: -76.30434278660042,
      FR_FBG_BM_D13_2a: -117.93744084527525,
    },
    {
      timestamp: 1586952180000,
      FR_FBG_CL_D1_1a: -46.92987694273199,
      FR_FBG_CL_D1_1b: -76.16050067776813,
      FR_FBG_BM_D13_2a: -117.65127509368841,
    },
    {
      timestamp: 1586952240000,
      FR_FBG_CL_D1_1a: -46.58616469604393,
      FR_FBG_CL_D1_1b: -75.80792018077112,
      FR_FBG_BM_D13_2a: -117.56199429165379,
    },
    {
      timestamp: 1586952300000,
      FR_FBG_CL_D1_1a: -46.75898317270426,
      FR_FBG_CL_D1_1b: -75.68596727762824,
      FR_FBG_BM_D13_2a: -117.66362073207115,
    },
    {
      timestamp: 1586952360000,
      FR_FBG_CL_D1_1a: -46.628079478715804,
      FR_FBG_CL_D1_1b: -75.46505461313707,
      FR_FBG_BM_D13_2a: -117.4428773429067,
    },
    {
      timestamp: 1586952420000,
      FR_FBG_CL_D1_1a: -46.684467892236945,
      FR_FBG_CL_D1_1b: -75.23350072668876,
      FR_FBG_BM_D13_2a: -117.29251790838654,
    },
    {
      timestamp: 1586952480000,
      FR_FBG_CL_D1_1a: -46.38250086337515,
      FR_FBG_CL_D1_1b: -75.10297851533076,
      FR_FBG_BM_D13_2a: -117.56320569229595,
    },
    {
      timestamp: 1586952540000,
      FR_FBG_CL_D1_1a: -46.47398840108186,
      FR_FBG_CL_D1_1b: -74.98095621767327,
      FR_FBG_BM_D13_2a: -117.19903839715609,
    },
  ]);
  const [mode, setMode] = useState(0); // 0 for Model, 1 for Chart
  const [dataType, setDataType] = useState("str");
  const [isLoading, setIsLoading] = useState(false);
  const [chartOptions, setChartOptions] = useState({
    sensors: [
      { name: "FR_FBG_CL_D1_1a", isSelected: true, colour: "blue" },
      { name: "FR_FBG_CL_D1_1b", isSelected: true, colour: "red" },
      { name: "FR_FBG_BM_D13_2a", isSelected: true, colour: "green" },
    ], // [{ name: sensorName, isSelected: true}, ... }]
    showTemperature: false,
    temperatureData: [
      {
        temperature: 10,
        timestamp: 1586952120000,
      },
      { temperature: 10.5, timestamp: 1586952300000 },
      { temperature: 11.0, timestamp: 1586952480000 },
    ], // [{temperature: x, timestamp: x}, ...]
  });
  const [modelOptions, setModelOptions] = useState({ showContext: true });

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
        <Model data={data} dataType={dataType}>
          {({ rotation, zoom, sensorColours }) => (
            <SteelFrame
              rotation={rotation}
              zoom={zoom}
              sensorColours={sensorColours}
              showContext={modelOptions.showContext}
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
        modelOptions={modelOptions}
        setModelOptions={setModelOptions}
      />
    </View>
  );
}
