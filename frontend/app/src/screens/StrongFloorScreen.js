import React from "react";
import { Canvas } from "react-three-fiber";

export default function StrongFloorScreen() {
  return (
    <Canvas camera={{ position: [0, 0, 50] }}>
      <ambientLight intensity={0.5} />
      <spotLight intensity={0.8} position={[300, 300, 400]} />
    </Canvas>
  );
}
