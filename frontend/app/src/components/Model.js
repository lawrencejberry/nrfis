import React, { Suspense, useState, useEffect } from "react";
import { View, Platform } from "react-native";
import * as THREE from "three";
import { Canvas } from "react-three-fiber";
import { Slider } from "react-native-elements";
import { State, PinchGestureHandler } from "react-native-gesture-handler";
import { XAxis } from "react-native-svg-charts";

import { LoadingIndicator } from "../models";
import formatTimestampLabel from "./utils";
import { theme } from "../utils";

window.performance = {
  clearMeasures: () => {},
  clearMarks: () => {},
  measure: () => {},
  mark: () => {},
  now: () => {},
};

export default function Model(props) {
  const [rotation, setRotation] = useState(new THREE.Euler(0, 0));
  const [sensorColours, setSensorColours] = useState({});
  const [index, setIndex] = useState(0);
  const [zoom, setZoom] = useState(1);
  const [baseZoom, setBaseZoom] = useState(1);

  const mapColour = (value) => {
    const min = props.modelOptions.scale[0];
    const max = props.modelOptions.scale[1];

    if (value < max && value > min) {
      const hue = (1 - (value - min) / (max - min)) * 270;
      return `hsl(${hue},100%,50%)`;
    }

    return "grey";
  };

  useEffect(() => {
    if (props.data.length) {
      const colours = Object.fromEntries(
        Object.entries(props.data[index]).map(([sensor, value]) => [
          sensor,
          mapColour(value),
        ])
      );
      setSensorColours(colours);
    }
  }, [
    props.data,
    props.modelOptions.colourMode,
    props.modelOptions.scale,
    index,
  ]);

  function handleResponderMove(event) {
    const touchBank =
      event.touchHistory.touchBank[Platform.select({ default: 0, ios: 1 })];
    const changeX = (touchBank.currentPageX - touchBank.previousPageX) / 200;
    const changeY = (touchBank.currentPageY - touchBank.previousPageY) / 200;
    setRotation(new THREE.Euler(rotation.x + changeY, rotation.y + changeX));
  }

  const handlePinchGestureEvent = ({ nativeEvent: event }) => {
    const newZoom = baseZoom * event.scale ** 0.5;
    if (Math.abs(newZoom - zoom) > 0.02 && newZoom > 0.2 && newZoom < 5) {
      setZoom(newZoom);
    }
  };

  const handleStateChange = ({ nativeEvent: event }) => {
    if (event.oldState === State.ACTIVE) {
      setBaseZoom(zoom);
    }
  };

  return (
    <PinchGestureHandler
      onGestureEvent={handlePinchGestureEvent}
      onHandlerStateChange={handleStateChange}
    >
      <View
        style={{ flex: 1 }}
        onMoveShouldSetResponder={(_) => true}
        onResponderMove={(event) => handleResponderMove(event)}
      >
        <Canvas style={{ flex: 8 }} camera={{ position: [0, 0, 40] }}>
          <ambientLight intensity={0.5} />
          <spotLight intensity={0.8} position={[300, 300, 400]} />
          <Suspense fallback={<LoadingIndicator />}>
            {props.children({ rotation, zoom, sensorColours })}
          </Suspense>
        </Canvas>
        <View style={{ flex: 1, marginHorizontal: 30, marginVertical: 5 }}>
          <Slider
            value={index}
            onValueChange={(value) => setIndex(value)}
            maximumValue={props.data.length ? props.data.length - 1 : 0}
            step={1}
            thumbStyle={{ backgroundColor: theme.colors.primary }}
          />
          <XAxis
            style={{ flex: 1 }}
            data={props.data}
            xAccessor={({ item }) => item.timestamp}
            formatLabel={formatTimestampLabel}
            svg={{ fontSize: 10, fill: theme.colors.primary }}
            numberOfTicks={5}
          />
        </View>
      </View>
    </PinchGestureHandler>
  );
}
