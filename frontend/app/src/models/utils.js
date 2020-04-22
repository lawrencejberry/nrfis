import React from "react";

/*
This function return a Three.js material coloured according to the map
of sensor colours and a given list of sensor names. The function will try accessing
the map with each name until it finds a match, at which point it will return a material
of that colour.

In this way, a Three.js object which represents both a strain and a temperature sensor
can be coloured just by supplying the names used in both cases to the sensorNames array.
This avoids having to check the dataType, and allows us to pass in multiple alternative
names for each sensor in case they change in a future version of the NRFIS API.
*/

export function renderSensorColour(sensorColours, sensorNames) {
  sensorNames = Array.isArray(sensorNames) ? sensorNames : [sensorNames]; // To allow specifying a single sensor name not as an array

  for (const sensorName of sensorNames) {
    if (sensorColours[sensorName]) {
      return (
        <meshBasicMaterial
          attach="material"
          color={sensorColours[sensorName]}
        />
      );
    }
  }
  return <meshBasicMaterial attach="material" transparent={true} opacity={0} />;
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
