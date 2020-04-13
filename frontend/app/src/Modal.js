import React, { useState, useEffect, useRef } from "react";
import {
  Animated,
  Easing,
  StyleSheet,
  Dimensions,
  Modal as ReactNativeModal,
  Text,
  View,
  TouchableWithoutFeedback,
  TouchableHighlight
} from "react-native";

const BORDER_RADIUS = 13;
const BACKGROUND_COLOR_LIGHT = "white";
const BORDER_COLOR = "#d5d5d5";
const TITLE_FONT_SIZE = 20;
const TITLE_COLOR = "#8f8f8f";
const BUTTON_FONT_COLOR = "#007ff9";
const BUTTON_FONT_SIZE = 20;
const HIGHLIGHT_COLOR_LIGHT = "#ebebeb";

const Header = ({ label }) => {
  return (
    <View
      style={{
        borderBottomColor: BORDER_COLOR,
        borderBottomWidth: StyleSheet.hairlineWidth,
        padding: 14,
        backgroundColor: "transparent"
      }}
    >
      <Text
        style={{
          textAlign: "center",
          color: TITLE_COLOR,
          fontSize: TITLE_FONT_SIZE
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
        backgroundColor: BACKGROUND_COLOR_LIGHT
      }}
      underlayColor={HIGHLIGHT_COLOR_LIGHT}
      onPress={onPress}
    >
      <Text
        style={{
          padding: 10,
          textAlign: "center",
          color: BUTTON_FONT_COLOR,
          fontSize: BUTTON_FONT_SIZE,
          fontWeight: "600",
          backgroundColor: "transparent"
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
      // Using native driver in the modal makes the content flash
      useNativeDriver: false,
      duration: 300,
      toValue: 1
    }).start();
  };

  hide = () => {
    Animated.timing(animVal, {
      easing: Easing.inOut(Easing.quad),
      // Using native driver in the modal makes the content flash
      useNativeDriver: false,
      duration: 300,
      toValue: 0
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
            width: Dimensions.get("window").width,
            height: Dimensions.get("window").height,
            position: "absolute",
            backgroundColor: "black",
            opacity: animVal.interpolate({
              inputRange: [0, 1],
              outputRange: [0, 0.4]
            })
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
                  extrapolate: "clamp"
                })
              }
            ]
          }}
          pointerEvents="box-none"
        >
          <View
            style={{
              borderRadius: BORDER_RADIUS,
              marginBottom: 8,
              overflow: "hidden",
              backgroundColor: BACKGROUND_COLOR_LIGHT
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
