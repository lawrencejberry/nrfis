import React, { useContext, useEffect, useRef } from "react";
import { View, Image, Text, Animated } from "react-native";
import { Header as HeaderBar, Icon } from "react-native-elements";

import { theme, LiveStatusContext } from "../utils";

export default function Header() {
  const { live } = useContext(LiveStatusContext);

  opacity = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, {
          toValue: 0,
          duration: 600,
          useNativeDriver: true,
        }),
        Animated.timing(opacity, {
          toValue: 1,
          delay: 200,
          duration: 600,
          useNativeDriver: true,
        }),
      ])
    ).start();
  });

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
        <View style={{ flex: 10, flexDirection: "row", alignItems: "center" }}>
          {live ? (
            <View
              style={{
                flexDirection: "row",
                alignItems: "center",
                marginRight: 20,
              }}
            >
              <Text
                style={{
                  marginRight: 5,
                  marginBottom: 2,
                  color: "white",
                }}
              >
                Live
              </Text>
              <Animated.View style={{ opacity: opacity }}>
                <Icon name="controller-record" type="entypo" color="#f54842" />
              </Animated.View>
            </View>
          ) : null}

          <Image
            source={require("../../assets/images/cambridge.png")}
            style={{ width: 100, height: 20, marginBottom: 2 }}
          />
        </View>
      }
    />
  );
}
