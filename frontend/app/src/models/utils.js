import React from "react";

export function renderSensorColour(sensorColours, sensor) {
  if (sensorColours) {
    return (
      <meshBasicMaterial attach="material" color={sensorColours[sensor]} />
    );
  } else {
    return null;
  }
}
