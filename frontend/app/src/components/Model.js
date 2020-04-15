import React, { Suspense, useState, useEffect } from "react";
import { View, Platform } from "react-native";
import { Asset } from "expo-asset";
import * as THREE from "three";
import { Canvas } from "react-three-fiber";
import { Slider } from "react-native-elements";

import { LoadingIndicator } from "../models";
import { theme } from "../utils";

window.performance = {
  clearMeasures: () => {},
  clearMarks: () => {},
  measure: () => {},
  mark: () => {},
  now: () => {},
};

function mapColour(dataType, v) {
  if (dataType == "str") {
    if (v < -200) return "grey";
    else if (v > 200) return "grey";
    else {
      const hue = (1 - (v + 200) / 400) * 270;
      return `hsl(${hue},100%,50%)`;
    }
  } else if (dataType == "tmp") {
    if (v < -10) return "grey";
    else if (v > 10) return "grey";
    else {
      const hue = (1 - (v + 10) / 20) * 270;
      return `hsl(${hue},100%,50%)`;
    }
  }
}

export default function Model(props) {
  const { children, file, ...rest } = props;
  const [localUri, setLocalUri] = useState("");
  const [rotation, setRotation] = useState(new THREE.Euler(0, 0));
  const [sensorColours, setSensorColours] = useState({});
  const [index, setIndex] = useState(0);

  useEffect(() => {
    (async (file) => {
      const asset = Asset.fromModule(file);
      await asset.downloadAsync();
      setLocalUri(asset.localUri);
    })(props.file);
  }, [props.file]);

  useEffect(() => {
    if (Array.isArray(props.data) && props.data.length) {
      const colours = Object.fromEntries(
        Object.entries(props.data[index]).map(([k, v]) => [
          k,
          mapColour(props.dataType, v),
        ])
      );
      setSensorColours(colours);
    }
  }, [props.data, index]);

  function handleResponderMove(event) {
    const touchBank =
      event.touchHistory.touchBank[Platform.select({ default: 0, ios: 1 })];
    const changeX = (touchBank.currentPageX - touchBank.previousPageX) / 200;
    const changeY = (touchBank.currentPageY - touchBank.previousPageY) / 200;
    setRotation(new THREE.Euler(rotation.x + changeY, rotation.y + changeX));
  }

  return (
    <View
      style={{ flex: 1 }}
      onMoveShouldSetResponder={(event) => true}
      onResponderMove={(event) => handleResponderMove(event)}
      {...rest}
    >
      <Slider
        value={index}
        onValueChange={(value) => setIndex(value)}
        maximumValue={props.data.length ? props.data.length - 1 : 0}
        step={1}
        style={{
          marginLeft: 20,
          marginRight: 20,
          marginTop: 10,
          marginBottom: 10,
        }}
        thumbStyle={{ backgroundColor: theme.colors.primary }}
      />
      <Canvas camera={{ position: [0, 0, 40] }}>
        <ambientLight intensity={0.5} />
        <spotLight intensity={0.8} position={[300, 300, 400]} />
        <Suspense fallback={<LoadingIndicator />}>
          {props.children({ localUri, rotation, sensorColours })}
        </Suspense>
      </Canvas>
    </View>
  );
}
