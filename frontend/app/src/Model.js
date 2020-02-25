import React, { Suspense, useState, useEffect } from "react";
import { View } from "react-native";
import { Asset } from "expo-asset";
import * as THREE from "three";
import { Canvas } from "react-three-fiber";

import SteelFrame from "./models/SteelFrame";

window.performance = {
  clearMeasures: () => {},
  clearMarks: () => {},
  measure: () => {},
  mark: () => {},
  now: () => {}
};

export default function Model() {
  const [localUri, setLocalUri] = useState("");
  const [rotation, setRotation] = useState(new THREE.Euler(0, 0));

  useEffect(() => {
    (async () => {
      const asset = Asset.fromModule(
        require("../assets/models/steel-frame.glb")
      );
      await asset.downloadAsync();
      setLocalUri(asset.localUri);
    })();
  }, []);

  function handleResponderMove(event) {
    const touchBank = event.touchHistory.touchBank[1];
    const changeX = (touchBank.currentPageX - touchBank.startPageX) / 2000;
    const changeY = (touchBank.currentPageY - touchBank.startPageY) / 2000;
    setRotation(new THREE.Euler(rotation.x + changeY, rotation.y + changeX));
  }

  return (
    <View
      style={{ flex: 1 }}
      onMoveShouldSetResponder={event => true}
      onResponderMove={event => handleResponderMove(event)}
    >
      <Canvas camera={{ position: [0, 0, 50] }}>
        <ambientLight intensity={0.5} />
        <spotLight intensity={0.8} position={[300, 300, 400]} />
        <Suspense fallback={<></>}>
          {localUri ? (
            <SteelFrame localUri={localUri} rotation={rotation} />
          ) : null}
        </Suspense>
      </Canvas>
    </View>
  );
}
