import React, { useState, useEffect, useRef } from "react";
import {
  Animated,
  Easing,
  StyleSheet,
  Dimensions,
  Platform,
  Modal as ReactNativeModal,
  View,
  TouchableWithoutFeedback,
  TouchableHighlight,
} from "react-native";
import { Text } from "react-native-elements";

import { theme } from "../utils";

const BORDER_RADIUS = 13;
const BACKGROUND_COLOR_LIGHT = theme.colors.background;
const BORDER_COLOR = theme.colors.border;
const FONT_SIZE = Platform.select({ default: 14, ios: 18 });
const BUTTON_FONT_COLOR = theme.colors.actionable;
const HIGHLIGHT_COLOR_LIGHT = "#ebebeb";

const Header = ({ label }) => {
  return (
    <View
      style={{
        borderBottomColor: BORDER_COLOR,
        borderBottomWidth: StyleSheet.hairlineWidth,
        padding: 14,
        backgroundColor: "transparent",
      }}
    >
      <Text
        style={{
          textAlign: "center",
          color: theme.colors.primary,
          fontSize: FONT_SIZE,
          fontWeight: "400",
        }}
      >
        {label}
      </Text>
    </View>
  );
};

const ConfirmButton = ({ onPress, label }) => {
  return (
    <TouchableHighlight
      style={{
        borderRadius: BORDER_RADIUS,
        height: 57,
        marginBottom: 0,
        justifyContent: "center",
        backgroundColor: BACKGROUND_COLOR_LIGHT,
      }}
      underlayColor={HIGHLIGHT_COLOR_LIGHT}
      onPress={onPress}
    >
      <Text
        style={{
          padding: 10,
          textAlign: "center",
          color: BUTTON_FONT_COLOR,
          fontSize: FONT_SIZE,
          fontWeight: "600",
          backgroundColor: "transparent",
        }}
      >
        {label}
      </Text>
    </TouchableHighlight>
  );
};

export default function Modal(props) {
  const { width, height, isActive, label, handleConfirm, children } = props;

  const [isVisible, setIsVisible] = useState(false);

  animVal = useRef(new Animated.Value(0)).current;

  show = () => {
    setIsVisible(true);
    Animated.timing(animVal, {
      easing: Easing.inOut(Easing.quad),
      useNativeDriver: true,
      duration: 300,
      toValue: 1,
    }).start();
  };

  hide = () => {
    Animated.timing(animVal, {
      easing: Easing.inOut(Easing.quad),
      useNativeDriver: true,
      duration: 300,
      toValue: 0,
    }).start(() => {
      setIsVisible(false);
    });
  };

  useEffect(() => {
    if (isActive) {
      show();
    } else {
      hide();
    }
  }, [isActive]);

  return (
    <ReactNativeModal transparent animationType="none" visible={isVisible}>
      <TouchableWithoutFeedback>
        <Animated.View
          style={{
            width: Dimensions.get("screen").width,
            height: Dimensions.get("screen").height,
            position: "absolute",
            backgroundColor: "black",
            opacity: animVal.interpolate({
              inputRange: [0, 1],
              outputRange: [0, 0.4],
            }),
          }}
        />
      </TouchableWithoutFeedback>
      {isVisible && (
        <Animated.View
          style={{
            flex: 1,
            width: width,
            justifyContent: "flex-end",
            alignSelf: "flex-end",
            padding: 10,
            transform: [
              {
                translateY: animVal.interpolate({
                  inputRange: [0, 1],
                  outputRange: [height, 0],
                  extrapolate: "clamp",
                }),
              },
            ],
          }}
          pointerEvents="box-none"
        >
          <View
            style={{
              maxHeight: height - 12,
              borderRadius: BORDER_RADIUS,
              marginBottom: 8,
              overflow: "hidden",
              backgroundColor: BACKGROUND_COLOR_LIGHT,
              paddingHorizontal: 12,
            }}
          >
            <Header label={label} />
            {children}
          </View>
          <ConfirmButton onPress={handleConfirm} label="Confirm" />
        </Animated.View>
      )}
    </ReactNativeModal>
  );
}
