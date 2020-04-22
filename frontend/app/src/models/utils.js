import React from "react";

/*
This function return a Three.js material coloured according to the map
of sensor colours and a given sensor name.
*/
export function renderSensorColour(sensorColours, sensorName) {
  return (
    <meshBasicMaterial
      attach="material"
      color={sensorColours[sensorName] ? sensorColours[sensorName] : "white"}
    />
  );
}

export function renderSensor(sensorColours, sensorName, position, size) {
  if (sensorColours[sensorName]) {
    return (
      <mesh visible position={position}>
        <boxGeometry attach="geometry" args={size} />
        <meshBasicMaterial
          attach="material"
          color={sensorColours[sensorName]}
        />
      </mesh>
    );
  }
  return null;
}
