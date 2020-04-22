import React, { useContext } from "react";
import { Image } from "react-native";
import { Header as HeaderBar } from "react-native-elements";

import { theme, LiveStatusContext } from "../utils";

export default function Header() {
  const liveStatus = useContext(LiveStatusContext);

  return (
    <HeaderBar
      containerStyle={{
        height: 70,
        paddingVertical: 20,
        paddingHorizontal: 20,
        borderBottomColor: theme.colors.secondary,
      }}
      statusBarProps={{
        hidden: true,
      }}
      placement="left"
      backgroundColor={theme.colors.secondary}
      leftComponent={
        <Image
          source={require("../../assets/images/logo.png")}
          style={{ width: 75, height: 55 }}
        />
      }
      centerComponent={
        <Image
          source={require("../../assets/images/title.png")}
          style={{ width: 60, height: 10 }}
        />
      }
      rightComponent={
        <Image
          source={require("../../assets/images/cambridge.png")}
          style={{ width: 100, height: 20 }}
        />
      }
    />
  );
}
