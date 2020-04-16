import React, { useState, useEffect } from "react";
import { View } from "react-native";
import { Text } from "react-native-elements";
import { TSpan, Circle } from "react-native-svg";
import { LineChart, Grid, YAxis, XAxis } from "react-native-svg-charts";
import * as D3 from "d3-shape";

import { theme } from "../utils";

const contentInset = { top: 10, bottom: 10, left: 5, right: 5 };

const Decorator = ({ x, y, data: datasets, timestamps }) =>
  datasets.map(({ data, svg, label }) =>
    data.map((value, index) => (
      <Circle
        key={label + index}
        cx={x(timestamps[index])}
        cy={y(value)}
        r={3}
        stroke={svg.stroke}
        fill={"white"}
      />
    ))
  );

export default function Chart(props) {
  const [datasets, setDatasets] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [range, setRange] = useState([0, 10]);

  useEffect(() => {
    setDatasets(
      props.sensors
        .filter(({ isSelected }) => isSelected)
        .map(({ name, colour }) => ({
          data: props.data.map((sample) => sample[name]),
          svg: { stroke: colour },
          label: name,
        }))
    );
  }, [props.data, props.sensors]);

  useEffect(() => {
    setTimestamps(props.data.map((sample) => Date.parse(sample.timestamp))); // Store times as Unix timestamps
    setRange([timestamps[0], timestamps[props.data.length - 1]]);
  }, [props.data]);

  // If no data is currently set
  if (!datasets.length) {
    return (
      <Text style={{ alignSelf: "center", marginTop: "40%" }}>
        Click Refresh to load data
      </Text>
    );
  }

  const formatTimestampLabel = (value) => {
    const datetime = new Date(value).toUTCString();
    const date = datetime.slice(5, 16);
    const time = datetime.slice(17, -4);
    return (
      <>
        <TSpan>{time}</TSpan>
        <TSpan dx="-4.3em" dy="1.2em">
          {date}
        </TSpan>
      </>
    );
  };

  return (
    <View style={{ flex: 1, flexDirection: "row", padding: 20 }}>
      <YAxis
        style={{ flex: 1 }}
        data={datasets.reduce((acc, dataset) => acc.concat(dataset.data), [])}
        contentInset={contentInset}
        svg={{ fontSize: 10, fill: theme.colors.primary }}
        numberOfTicks={10}
      />
      <View style={{ flex: 30, marginLeft: 10 }}>
        <LineChart
          style={{ flex: 30 }}
          data={datasets}
          xAccessor={({ index }) => timestamps[index]}
          contentInset={contentInset}
          curve={D3.curveBasis}
        >
          <Grid direction={Grid.Direction.HORIZONTAL} />
          <Decorator timestamps={timestamps} />
        </LineChart>
        <XAxis
          style={{ flex: 1 }}
          data={timestamps}
          xAccessor={({ item }) => item}
          formatLabel={formatTimestampLabel}
          contentInset={contentInset}
          svg={{ fontSize: 10, fill: theme.colors.primary }}
          numberOfTicks={5}
        />
      </View>
    </View>
  );
}
