import React from "react";
import { View } from "react-native";
import { Button } from "react-native-elements";

export default function Menu(props) {
  return (
    <View {...props}>
      <Button title="Solid Button" />
    </View>
  );
}
