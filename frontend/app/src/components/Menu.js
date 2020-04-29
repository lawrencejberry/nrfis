import React, { useState } from "react";
import {
  Platform,
  View,
  Picker as WheelPickerIOS,
  ScrollView,
} from "react-native";
import {
  Divider,
  Button,
  ButtonGroup,
  ListItem,
  Text,
} from "react-native-elements";
import DateTimePickerIOS from "@react-native-community/datetimepicker";
import { DateTimePickerModal as DateTimePickerAndroid } from "react-native-modal-datetime-picker";
import { LinearGradient } from "expo-linear-gradient";
import { XAxis } from "react-native-svg-charts";

import Modal from "./Modal";
import { theme, modelColourScale, labels } from "../utils";

const MultiSelect = ({ options, setOptions }) => (
  <ScrollView style={{ maxHeight: "100%" }}>
    {options.map(({ name, isSelected }, index) => {
      return (
        <ListItem
          contentContainerStyle={{ padding: 2 }}
          key={name}
          title={name}
          onPress={() =>
            setOptions(
              options.map((option, i) =>
                i === index ? { ...option, isSelected: !isSelected } : option
              )
            )
          }
          checkmark={isSelected}
        />
      );
    })}
  </ScrollView>
);

const Picker = ({ value, setValue, options }) => {
  if (Platform.OS === "ios") {
    return (
      <WheelPickerIOS
        selectedValue={value}
        onValueChange={(itemValue, _) => setValue(itemValue)}
      >
        {options.map((option) => (
          <WheelPickerIOS.Item
            label={option.label}
            value={option.value}
            key={option.value}
          />
        ))}
      </WheelPickerIOS>
    );
  } else if (Platform.OS === "android") {
    return (
      <ScrollView style={{ maxHeight: "100%" }}>
        {options.map((option, _) => (
          <ListItem
            key={option.value}
            title={option.label}
            onPress={() => setValue(option.value)}
            checkmark={option.value === value}
          />
        ))}
      </ScrollView>
    );
  }
};

const DateTimePicker = ({ datetime, setDatetime, ...dialogProps }) => {
  if (Platform.OS === "ios") {
    return (
      <DateTimePickerIOS
        mode="datetime"
        timeZoneOffsetInMinutes={0}
        value={datetime}
        onChange={(_, dt) => setDatetime(dt)}
      />
    );
  } else if (Platform.OS === "android") {
    return (
      <DateTimePickerAndroid
        mode="datetime"
        date={datetime}
        isVisible={dialogProps.isActive}
        onCancel={() => null}
        onConfirm={(dt) => {
          dialogProps.handleConfirm();
          setDatetime(dt);
        }}
        is24hour={true}
      />
    );
  }
};

const Dialog = ({ children, ...props }) => {
  if (props.isActive) {
    return children(props);
  } else {
    return null;
  }
};

export default function Menu(props) {
  const [dataType, setDataType] = useState("str");
  const [averagingWindow, setAveragingWindow] = useState("");
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());

  const [shownElement, setShownElement] = useState("");
  const [isModalActive, setIsModalActive] = useState(false);
  const [isDialogActive, setIsDialogActive] = useState(false);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);

  function showSelector(shownElement) {
    setShownElement(shownElement);
    // Set dialog or modal active depending on platform and selector
    if (
      Platform.OS === "android" &&
      ["Start Time", "End Time"].includes(shownElement)
    ) {
      setIsDialogActive(true);
    } else {
      setIsModalActive(true);
    }
  }

  function renderButton(element, value) {
    let label = value;
    if (value && Object.keys(labels).includes(element)) {
      label = labels[element].find((element) => element.value === value).label;
    }
    if (value instanceof Date) {
      label = value.toUTCString();
    }
    return (
      <Button
        key={element}
        title={`${element}${label ? `: ${label}` : ""}`}
        type={shownElement == element ? "solid" : "outline"}
        onPress={() => showSelector(element)}
        titleStyle={{
          fontWeight: "normal",
          color:
            shownElement == element
              ? theme.colors.background
              : theme.colors.secondary,
        }}
      />
    );
  }

  const renderModelMenu = () => (
    <>
      <Text>MODEL OPTIONS</Text>
      <Button
        title={props.modelOptions.showContext ? "Hide Context" : "Show Context"}
        type={props.modelOptions.showContext ? "solid" : "outline"}
        onPress={() =>
          props.setModelOptions({
            ...props.modelOptions,
            showContext: !props.modelOptions.showContext,
          })
        }
        titleStyle={{
          fontWeight: "normal",
          color: props.modelOptions.showContext
            ? theme.colors.background
            : theme.colors.secondary,
        }}
      />
      <Divider />
      <Text>COLOUR SCALE</Text>
      <ButtonGroup
        buttons={["Adaptive", "Absolute"]}
        selectedIndex={props.modelOptions.colourMode}
        disabled={props.liveMode ? [0] : []} // Adaptive button disabled when in live mode
        onPress={(index) =>
          props.setModelOptions({
            ...props.modelOptions,
            colourMode: index,
            scale: index
              ? modelColourScale[props.screenState.dataType]
              : props.dataRange,
          })
        }
      />
      <View style={{ flex: 1, paddingVertical: 5 }}>
        <LinearGradient
          style={{
            height: 40,
            marginHorizontal: 10,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: theme.colors.border,
          }}
          colors={[...Array(270).keys()]
            .reverse()
            .map((hue) => `hsl(${hue},100%,50%)`)}
          start={[0, 0.5]}
          end={[1, 0.5]}
        />
        <XAxis
          style={{ flex: 1, marginVertical: 8 }}
          data={props.modelOptions.scale}
          xAccessor={({ item }) => item}
          contentInset={{ left: 18, right: 18 }}
          svg={{ fontSize: 10, fill: theme.colors.primary }}
          numberOfTicks={5}
        />
      </View>
    </>
  );

  const renderChartMenu = () => (
    <>
      <Text>CHART OPTIONS</Text>
      {renderButton("Select Sensors")}
      {props.liveMode ? null : (
        <Button
          title={
            props.chartOptions.showTemperature
              ? "Hide Outdoor Temperature"
              : "Show Outdoor Temperature"
          }
          type={props.chartOptions.showTemperature ? "solid" : "outline"}
          onPress={() =>
            props.setChartOptions({
              ...props.chartOptions,
              showTemperature: !props.chartOptions.showTemperature,
            })
          }
          titleStyle={{
            fontWeight: "normal",
            color: props.chartOptions.showTemperature
              ? theme.colors.background
              : theme.colors.secondary,
          }}
        />
      )}
      <Divider />
      <Text>LEGEND</Text>
      <View
        style={{
          flex: 1,
          flexDirection: "row",
          flexWrap: "wrap",
          alignItems: "flex-start",
          marginBottom: 20,
        }}
      >
        {props.chartOptions.sensors
          .filter(({ isSelected }) => isSelected)
          .map(({ name, colour }) => (
            <ListItem
              key={name}
              containerStyle={{
                minWidth: 150,
                maxWidth: 250,
                padding: 0,
                marginHorizontal: 10,
              }}
              title={name}
              titleStyle={{ fontSize: 12 }}
              rightIcon={{
                name: "minus",
                type: "feather",
                color: colour,
                size: 20,
              }}
            />
          ))}
        {props.chartOptions.showTemperature ? (
          <ListItem
            containerStyle={{
              minWidth: 150,
              maxWidth: 250,
              padding: 0,
              marginHorizontal: 10,
            }}
            title="OUTDOOR TEMPERATURE"
            titleStyle={{ fontSize: 12 }}
            rightIcon={{
              name: "minus",
              type: "feather",
              color: "orange",
              size: 20,
            }}
          />
        ) : null}
      </View>
    </>
  );

  function renderModalSelector(shownElement) {
    switch (shownElement) {
      case "Data Type":
        return (
          <Picker
            value={props.liveMode ? props.screenState.liveDataType : dataType}
            setValue={
              props.liveMode
                ? (liveDataType) =>
                    props.setScreenState({ ...props.screenState, liveDataType })
                : setDataType
            }
            options={labels["Data Type"]}
          />
        );
      case "Averaging Window":
        return (
          <Picker
            value={averagingWindow}
            setValue={setAveragingWindow}
            options={labels["Averaging Window"]}
          />
        );
      case "Start Time":
        return (
          <DateTimePicker datetime={startTime} setDatetime={setStartTime} />
        );
      case "End Time":
        return <DateTimePicker datetime={endTime} setDatetime={setEndTime} />;
      case "Select Sensors":
        return (
          <MultiSelect
            options={props.chartOptions.sensors}
            setOptions={(sensors) =>
              props.setChartOptions({ ...props.chartOptions, sensors: sensors })
            }
          />
        );
      default:
        return null;
    }
  }

  function renderDialogSelector(shownElement, dialogProps) {
    switch (shownElement) {
      case "Start Time":
        return (
          <DateTimePicker
            {...dialogProps}
            datetime={startTime}
            setDatetime={setStartTime}
          />
        );

      case "End Time":
        return (
          <DateTimePicker
            {...dialogProps}
            datetime={endTime}
            setDatetime={setEndTime}
          />
        );
      default:
        return null;
    }
  }

  function modelModeDisabled() {
    const dt = props.liveMode
      ? props.screenState.liveDataType
      : props.screenState.dataType;
    return dt !== "raw" ? [] : [0];
  }

  return (
    <ScrollView
      style={props.style}
      onLayout={(event) => {
        setWidth(event.nativeEvent.layout.width);
        setHeight(event.nativeEvent.layout.height);
      }}
    >
      <ButtonGroup
        buttons={["Model", "Chart"]}
        selectedIndex={props.mode}
        disabled={modelModeDisabled()} // Model mode only enabled for str or tmp
        onPress={(index) => props.setMode(index)}
      />
      <Divider />
      <Text>DATA OPTIONS</Text>
      <ButtonGroup
        buttons={["Live", "Historical"]}
        selectedIndex={props.liveMode ? 0 : 1} // 0 = Live, 1 = Historical
        disabled={props.live ? [] : [0]} // Live button disabled when live mode is unavailable
        onPress={(index) =>
          index ? props.setLiveMode(false) : props.setLiveMode(true)
        }
      />
      {renderButton(
        "Data Type",
        props.liveMode
          ? props.screenState.liveDataType
          : props.screenState.dataType
      )}
      {props.liveMode ? null : (
        <>
          {[
            ["Averaging Window", props.screenState.averagingWindow],
            ["Start Time", props.screenState.startTime],
            ["End Time", props.screenState.endTime],
          ].map(([element, value]) => renderButton(element, value))}
          <Button
            title="Refresh"
            onPress={() => {
              props.refresh(dataType, averagingWindow, startTime, endTime);
            }}
            type="outline"
            titleStyle={{ color: theme.colors.actionable }}
            buttonStyle={{ borderColor: theme.colors.actionable }}
            loading={props.isLoading}
            loadingProps={{ size: 16 }}
          />
        </>
      )}
      <Divider />
      {props.mode ? renderChartMenu() : renderModelMenu()}
      <Modal
        label={shownElement}
        width={width}
        height={height}
        isActive={isModalActive}
        handleConfirm={() => {
          setIsModalActive(false);
          setShownElement("");
        }}
      >
        {renderModalSelector(shownElement)}
      </Modal>
      <Dialog
        isActive={isDialogActive}
        handleConfirm={() => {
          setIsDialogActive(false);
          setShownElement("");
        }}
      >
        {(dialogProps) => renderDialogSelector(shownElement, dialogProps)}
      </Dialog>
    </ScrollView>
  );
}
