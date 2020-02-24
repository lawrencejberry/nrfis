import React, { Suspense, useState, useEffect } from 'react';
import { Canvas } from "react-three-fiber"
import { Asset } from "expo-asset";

import Model from './SteelFrame'


window.performance = {
  clearMeasures: () => { },
  clearMarks: () => { },
  measure: () => { },
  mark: () => { },
  now: () => { },
}

export default function App() {
  const [uri, setUri] = useState("")

  useEffect(() => {
    (async () => {
      const asset = Asset.fromModule(require("./assets/models/steel-frame.glb"))
      await asset.downloadAsync()
      setUri(asset.localUri)
    })()
  }, [])

  return (
    <Canvas camera={{ position: [0, 0, 80] }}>
      <ambientLight intensity={0.5} />
      <spotLight intensity={0.8} position={[300, 300, 400]} />
      <Suspense fallback={<></>}>
        {(uri) ? (
          <Model uri={uri} position={[0, -20, 0]} />
        ) : null}
      </Suspense>
    </Canvas>
  )
}
