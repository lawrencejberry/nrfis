import React, { useState, useContext, useEffect, useRef } from "react";
import { View, Image, Text, Animated } from "react-native";
import { Header as HeaderBar, Icon } from "react-native-elements";

import HelpOverlay from "./HelpOverlay";
import { theme, LiveStatusContext } from "../utils";

export default function Header() {
  const [showHelp, setShowHelp] = useState(false);

  const { live } = useContext(LiveStatusContext);

  opacity = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, {
          toValue: 0,
          duration: 600,
          useNativeDriver: false,
        }),
        Animated.timing(opacity, {
          toValue: 1,
          delay: 200,
          duration: 600,
          useNativeDriver: false,
        }),
      ])
    );
    if (live) {
      animation.start();
    }
    return () => animation.stop();
  }, [live]);

  return (
    <>
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
          <View
            style={{ flex: 10, flexDirection: "row", alignItems: "center" }}
          >
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
                {live ? "Live" : "Not live"}
              </Text>
              <Animated.View style={{ opacity: opacity }}>
                <Icon
                  name="controller-record"
                  type="entypo"
                  color={live ? "#f54842" : theme.colors.primary}
                />
              </Animated.View>
            </View>
            <Icon
              containerStyle={{ marginRight: 20 }}
              name="help-with-circle"
              type="entypo"
              color="white"
              underlayColor={"transparent"}
              onPress={() => setShowHelp(!showHelp)}
            />
            <Image
              source={require("../../assets/images/cambridge.png")}
              style={{ width: 100, height: 20, marginBottom: 2 }}
            />
          </View>
        }
      />
      <HelpOverlay isActive={showHelp} setIsActive={setShowHelp} />
    </>
  );
}
