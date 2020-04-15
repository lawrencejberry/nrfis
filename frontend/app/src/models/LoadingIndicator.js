import React, { useRef } from "react";
import { useFrame } from "react-three-fiber";

import { theme } from "../utils";

export default function LoadingIndicator() {
  // This reference will give us direct access to the mesh
  const mesh = useRef();

  // Rotate mesh every frame, this is outside of React without overhead
  useFrame(() => (mesh.current.rotation.x = mesh.current.rotation.y += 0.01));

  return (
    <mesh ref={mesh} position={[0, 0, 0]}>
      <icosahedronBufferGeometry attach="geometry" args={[5]} />
      <meshStandardMaterial attach="material" color={theme.colors.primary} />
    </mesh>
  );
}
