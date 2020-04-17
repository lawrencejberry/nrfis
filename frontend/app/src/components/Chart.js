import React, { useState, useEffect } from "react";
import { View } from "react-native";
import { Text } from "react-native-elements";
import {
  TSpan,
  Circle,
  G,
  Rect,
  Line,
  Text as SVGText,
} from "react-native-svg";
import { LineChart, Grid, YAxis, XAxis } from "react-native-svg-charts";
import * as D3 from "d3-shape";
import {
  State,
  PinchGestureHandler,
  PanGestureHandler,
} from "react-native-gesture-handler";

import { theme } from "../utils";

const contentInset = { top: 10, bottom: 10, left: 5, right: 5 };

const Decorator = ({ x, y, value, timestamp, colour }) => {
  const [showLabel, setShowLabel] = useState(false);
  const [timeoutID, setTimeoutID] = useState(0);

  const toggleLabel = () => {
    setShowLabel(true);
    clearTimeout(timeoutID);
    setTimeoutID(setTimeout(() => setShowLabel(false), 3000));
  };

  return (
    <G x={x(timestamp)} y={y(value)}>
      {showLabel ? (
        <>
          <Rect
            height={16}
            width={32}
            x={-16}
            y={-32}
            stroke={theme.colors.primary}
            fill={theme.colors.background}
            ry={6}
            rx={6}
          />
          <SVGText
            x={0}
            y={-21.5}
            fontSize={8}
            fontWeight={300}
            textAnchor="middle"
            fill={theme.colors.secondary}
          >
            {value.toPrecision(3)}
          </SVGText>
          <Line y1={0} y2={-16} stroke={theme.colors.primary} strokeWidth={1} />
        </>
      ) : null}
      <Circle r={12} fill={"transparent"} onPress={toggleLabel} />
      <Circle r={3} stroke={colour} fill={"white"} />
    </G>
  );
};

const Decorators = ({ x, y, data: datasets, timestamps }) =>
  datasets.map(({ data, svg, label }) =>
    data.map((value, index) => (
      <Decorator
        key={label + index}
        x={x}
        y={y}
        value={value}
        timestamp={timestamps[index]}
        colour={svg.stroke}
      />
    ))
  );

export default function Chart(props) {
  const { data, chartOptions } = props;

  const [width, setWidth] = useState(0);
  const [datasets, setDatasets] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [minX, setMinX] = useState(0);
  const [maxX, setMaxX] = useState(0);
  const [baseRange, setBaseRange] = useState([0, 0]);
  const [minInterval, setMinInterval] = useState(0);

  useEffect(() => {
    setDatasets(
      chartOptions.sensors
        .filter(({ isSelected }) => isSelected)
        .map(({ name, colour }) => ({
          data: data.map((sample) => sample[name]),
          svg: { stroke: colour },
          label: name,
        }))
    );
  }, [data, chartOptions]);

  useEffect(() => {
    setTimestamps(data.map((sample) => Date.parse(sample.timestamp))); // Store times as Unix timestamps
    setMinX(timestamps[0]);
    setMaxX(timestamps[data.length - 1]);
    setBaseRange([minX, maxX]);
    setMinInterval(
      Math.min(
        ...timestamps
          .map((timestamp, index) =>
            index ? timestamp - timestamps[index - 1] : null
          )
          .slice(1)
      )
    );
  }, [data]);

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

  const handlePinchGestureEvent = ({ nativeEvent: event }) => {
    const oldRange = baseRange[1] - baseRange[0];
    const newRange = oldRange * (1 / event.scale);
    const change = newRange - oldRange;
    const focalPoint = event.focalX / width; // as a fraction from min to max
    const newMinX = minX - change * focalPoint;
    const newMaxX = maxX + change * (1 - focalPoint);

    // Don't update if newRange is zoomed in beyond three points, or if there is less than a 1% change from the baseRange
    if (
      newMaxX - newMinX < 2 * minInterval ||
      Math.abs(change) < oldRange / 100
    ) {
      return;
    }
    if (newMinX >= timestamps[0]) {
      setMinX(newMinX);
    }
    if (newMaxX <= timestamps[timestamps.length - 1]) {
      setMaxX(newMaxX);
    }
  };

  const handlePanGestureEvent = ({ nativeEvent: event }) => {
    const oldRange = baseRange[1] - baseRange[0];
    const change = 0.2 * (event.translationX / width) * oldRange;
    const newMinX = minX - change;
    const newMaxX = maxX - change;

    if (
      newMinX >= timestamps[0] &&
      newMaxX <= timestamps[timestamps.length - 1] &&
      Math.abs(change) > oldRange / 100
    ) {
      setMinX(newMinX);
      setMaxX(newMaxX);
    }
  };

  const handleStateChange = ({ nativeEvent: event }) => {
    if (event.oldState === State.ACTIVE) {
      setBaseRange([minX, maxX]);
    }
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
      <PinchGestureHandler
        onGestureEvent={handlePinchGestureEvent}
        onHandlerStateChange={handleStateChange}
      >
        <PanGestureHandler
          onGestureEvent={handlePanGestureEvent}
          onHandlerStateChange={handleStateChange}
          maxPointers={1}
        >
          <View
            style={{ flex: 30, marginLeft: 10, marginRight: 10 }}
            onLayout={(event) => {
              setWidth(event.nativeEvent.layout.width);
            }}
          >
            <View style={{ flex: 30 }}>
              <LineChart
                style={{ position: "absolute", width: "100%", height: "100%" }}
                data={datasets}
                xAccessor={({ index }) => timestamps[index]}
                contentInset={contentInset}
                curve={D3.curveBasis}
                xMin={minX}
                xMax={maxX}
              >
                <Grid direction={Grid.Direction.HORIZONTAL} />
                <Decorators timestamps={timestamps} />
              </LineChart>
              {chartOptions.showTemperature ? (
                <LineChart
                  style={{
                    position: "absolute",
                    width: "100%",
                    height: "100%",
                  }}
                  data={chartOptions.temperatureData}
                  xAccessor={({ item }) => Date.parse(item.timestamp)}
                  yAccessor={({ item }) => item.temperature}
                  contentInset={contentInset}
                  curve={D3.curveBasis}
                  svg={{ stroke: "orange" }}
                  xMin={minX}
                  xMax={maxX}
                >
                  {chartOptions.temperatureData.map((item, index) => (
                    <Decorator
                      key={index}
                      value={item.temperature}
                      timestamp={Date.parse(item.timestamp)}
                      colour="orange"
                    />
                  ))}
                </LineChart>
              ) : null}
            </View>
            <XAxis
              style={{ flex: 1 }}
              data={baseRange}
              xAccessor={({ item }) => item}
              formatLabel={formatTimestampLabel}
              contentInset={contentInset}
              svg={{ fontSize: 10, fill: theme.colors.primary }}
              numberOfTicks={5}
            />
          </View>
        </PanGestureHandler>
      </PinchGestureHandler>
      {chartOptions.showTemperature ? (
        <YAxis
          style={{ flex: 1 }}
          data={chartOptions.temperatureData}
          yAccessor={({ item }) => item.temperature}
          contentInset={contentInset}
          svg={{ fontSize: 10, fill: theme.colors.primary }}
          numberOfTicks={10}
        />
      ) : (
        <View style={{ flex: 1 }} />
      )}
    </View>
  );
}
