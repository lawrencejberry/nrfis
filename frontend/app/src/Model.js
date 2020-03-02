import React, { Suspense, useState, useEffect } from "react";
import { View } from "react-native";
import { Asset } from "expo-asset";
import * as THREE from "three";
import { Canvas } from "react-three-fiber";
import { Slider } from "react-native-elements";

import { LoadingIndicator } from "./models";

window.performance = {
  clearMeasures: () => {},
  clearMarks: () => {},
  measure: () => {},
  mark: () => {},
  now: () => {}
};

function mapColour(dataType, v) {
  if (dataType == "str") {
    const absV = abs(v);
    if (absV < 1e6) return "hsl(90,100%,50%)";
    else if (absV > 1000e6) return "hsl(0,100%,50%)";
    else {
      const hue = (1 - (absV - 1e6) / 999e6) * 90;
      return `hsl(${hue},100%,50%)`;
    }
  } else if (dataType == "tmp") {
    if (v < -25.0) return "hsl(270,100%,50%)";
    else if (v > 25.0) return "hsl(0,100%,50%)";
    else {
      const hue = (1 - (v + 25) / 50.0) * 270;
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
    (async file => {
      const asset = Asset.fromModule(file);
      await asset.downloadAsync();
      setLocalUri(asset.localUri);
    })(props.file);
  }, [props.file]);

  useEffect(() => {
    if (props.data.length > 0) {
      const colours = Object.fromEntries(
        Object.entries(props.data[index]).map(([k, v]) => [k, mapColour(v)])
      );
      setSensorColours(colours);
    }
  }, [props.data, index]);

  function handleResponderMove(event) {
    const touchBank = event.touchHistory.touchBank[1];
    const changeX = (touchBank.currentPageX - touchBank.previousPageX) / 200;
    const changeY = (touchBank.currentPageY - touchBank.previousPageY) / 200;
    setRotation(new THREE.Euler(rotation.x + changeY, rotation.y + changeX));
  }

  return (
    <View
      style={{ flex: 5 }}
      onMoveShouldSetResponder={event => true}
      onResponderMove={event => handleResponderMove(event)}
      {...rest}
    >
      <Slider
        value={index}
        onValueChange={value => setIndex(value)}
        maximumValue={props.data.length ? props.data.length - 1 : 0}
        step={1}
        style={{
          marginLeft: 20,
          marginRight: 20,
          marginTop: 10,
          marginBottom: 10
        }}
        thumbStyle={{ backgroundColor: "grey" }}
      />
      <Canvas camera={{ position: [0, 0, 50] }}>
        <ambientLight intensity={0.5} />
        <spotLight intensity={0.8} position={[300, 300, 400]} />
        <Suspense fallback={<LoadingIndicator />}>
          {props.children({ localUri, rotation, sensorColours })}
        </Suspense>
      </Canvas>
    </View>
  );
}
