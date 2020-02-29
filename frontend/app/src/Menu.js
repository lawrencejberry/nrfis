import React from "react";
import { View, Picker, DatePicker } from "react-native";
import {
  Divider,
  Text,
  Button,
  ButtonGroup,
  Checkbox
} from "react-native-elements";
import { ListItem } from "react-native-elements";

const list = [
  {
    title: "Appointments",
    icon: "av-timer"
  },
  {
    title: "Trips",
    icon: "flight-takeoff"
  }
];
export default function Menu(props) {
  return (
    <View
      style={{
        flex: 2,
        borderLeftWidth: 2,
        borderColor: "#404040"
      }}
    >
      <ListItem title={"1"} switch bottomDivider />
      <ListItem
        title={"2"}
        buttonGroup={{ buttons: ["First", "Second"] }}
        bottomDivider
      />
      <ListItem title={"3"} checkBox bottomDivider />
    </View>
  );
}
