import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Modal,
  Animated,
  TouchableWithoutFeedback,
  Easing,
  Dimensions,
} from "react-native";
import { Text, Icon } from "react-native-elements";

const HelpText = ({ children, style }) => (
  <View
    style={{ flex: 1, flexDirection: "row", alignItems: "center", ...style }}
  >
    <Text style={{ color: "white" }}>{children}</Text>
    <Icon name="long-arrow-right" type="font-awesome" color="white" size={30} />
  </View>
);

export default function HelpOverlay({ isActive, setIsActive }) {
  const [isVisible, setIsVisible] = useState(false);

  const helpOverlayOpacity = useRef(new Animated.Value(0)).current;

  show = () => {
    setIsVisible(true);
    Animated.timing(helpOverlayOpacity, {
      easing: Easing.inOut(Easing.quad),
      useNativeDriver: true,
      duration: 300,
      toValue: 1,
    }).start();
  };

  hide = () => {
    Animated.timing(helpOverlayOpacity, {
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
    <Modal transparent animationType="none" visible={isVisible}>
      <>
        <Animated.View
          style={{
            width: Dimensions.get("window").width,
            height: Dimensions.get("window").height,
            position: "absolute",
            backgroundColor: "black",
            opacity: helpOverlayOpacity.interpolate({
              inputRange: [0, 1],
              outputRange: [0, 0.4],
            }),
          }}
        />
        <TouchableWithoutFeedback onPress={() => setIsActive(false)}>
          <Animated.View
            style={{
              flex: 1,
              opacity: helpOverlayOpacity,
            }}
          >
            <View
              style={{
                height: 70,
                flexDirection: "column",
              }}
            >
              <HelpText style={{ alignSelf: "flex-end", marginRight: 300 }}>
                Shows whether the system is currently recording
              </HelpText>
            </View>
            <View style={{ flex: 1, flexDirection: "row" }}>
              <View
                style={{
                  flex: 3,
                  alignItems: "flex-end",
                }}
              >
                <HelpText
                  style={{
                    flex: 1,
                    marginHorizontal: 20,
                  }}
                >
                  Model mode renders a 3D model of the building with coloured
                  sensors, "Chart" mode renders a scatter plot of the data
                </HelpText>
                <HelpText
                  style={{
                    flex: 2,
                    marginHorizontal: 20,
                  }}
                >
                  Select the data you wish to visualise
                </HelpText>
                <View
                  style={{
                    flex: 6,
                    padding: 20,
                    marginHorizontal: 20,
                    marginBottom: 20,
                    backgroundColor: "white",
                    borderRadius: 4,
                  }}
                >
                  <Text>
                    The National Research Facility for Infrastructure Sensing
                    (NRFIS) is a new state of the art research facility hosted
                    by the University of Cambridge. Housed in the new Civil
                    Engineering Building, NRFIS brings together specialist
                    engineering facilities and sensor development capabilities
                    under one roof. It offers an interdisciplinary centre for
                    cutting edge research to explore the development and
                    application of novel sensor systems at a range of scales.
                  </Text>
                  <Text>
                    The building is instrumented with six sensor packages, from
                    the roof to the foundations. The sensors are an integral
                    part of research being undertaken in Civil Engineering at
                    Cambridge and link closely to the Centre for Smart
                    Infrastructure and Construction (CSIC), also at the
                    University of Cambridge. We are developing the technologies
                    to display, store, interpret, and visualise these data
                    streams. This information will be used to understand the
                    performance of the new research facility and assess this
                    performance against the predictions made during design. By
                    examining any differences, we aim to understand performance,
                    and help improve future design.
                  </Text>
                  <Text>
                    This app serves as an interface into the building's fibre
                    optic FBG sensor monitoring system, which continuously
                    records strain and temperature change in the steel frame,
                    basement and strong floor. It offers a platform for
                    visualising the historical archive of data on interactive 3D
                    models and scatter plots, as well as real-time data when the
                    system is currently recording.
                  </Text>
                </View>
                <View
                  style={{
                    flex: 2,
                    padding: 20,
                    marginHorizontal: 20,
                    marginBottom: 90,
                    backgroundColor: "white",
                    borderRadius: 4,
                  }}
                >
                  <Text>Sensor naming conventions:</Text>
                  <Text>
                    Steel Frame: [BM/CL = Beam/Column] - [DX = Grid No.] - [X =
                    Floor] [a/b = Top/Bottom Flange]
                  </Text>
                  <Text>
                    Basement + Strong Floor: [EW/NS = East-West/North-South] -
                    [Str/Tmp = Strain/Temperature] - [bot/top = Bottom/Top] [X =
                    Index on Cable]
                  </Text>
                </View>
              </View>
              <View
                style={{
                  flex: 1,
                  minWidth: 100,
                  paddingVertical: 20,
                }}
              />
            </View>
          </Animated.View>
        </TouchableWithoutFeedback>
      </>
    </Modal>
  );
}
