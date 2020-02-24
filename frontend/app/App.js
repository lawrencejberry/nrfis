import React, { Suspense } from 'react';
import { Canvas } from "react-three-fiber";
import Model from './Model'

window.performance = {
  clearMeasures: () => { },
  clearMarks: () => { },
  measure: () => { },
  mark: () => { },
  now: () => { },
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 0, 50] }}>
      <ambientLight intensity={0.5} />
      <spotLight intensity={0.8} position={[300, 300, 400]} />
      <Suspense fallback={null}>
        <Model />
      </Suspense>
    </Canvas>
  )
}
