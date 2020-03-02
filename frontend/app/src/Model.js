import React, { Suspense, useState, useEffect } from "react";
import { View } from "react-native";
import { Asset } from "expo-asset";
import * as THREE from "three";
import { Canvas } from "react-three-fiber";

import { LoadingIndicator } from "./models";

window.performance = {
  clearMeasures: () => {},
  clearMarks: () => {},
  measure: () => {},
  mark: () => {},
  now: () => {}
};

export default function Model(props) {
  const { children, file, ...rest } = props;
  const [localUri, setLocalUri] = useState("");
  const [rotation, setRotation] = useState(new THREE.Euler(0, 0));
  const [sensorColours, setSensorColours] = useState({});

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
        Object.entries(props.data[0]).map(([k, v]) => [k, "red"])
      );
      setSensorColours(colours);
    }
  }, [props.data]);

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
