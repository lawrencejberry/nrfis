import React, { useState } from "react";
import { View } from "react-native";

export default function Chart() {
  const [width, setWidth] = useState(0);

  return (
    <View
      onLayout={(event) => {
        setWidth(event.nativeEvent.layout.width);
      }}
    ></View>
  );
}
