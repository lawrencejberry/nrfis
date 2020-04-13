import React, { useState } from "react";
import { View, Picker as ReactNativePicker } from "react-native";
import { Divider, Button, ButtonGroup } from "react-native-elements";
import DateTimePicker from "@react-native-community/datetimepicker";

import Modal from "./Modal";

const Picker = ({ value, setValue, options }) => (
  <ReactNativePicker
    selectedValue={value}
    onValueChange={(itemValue, _) => setValue(itemValue)}
  >
    {options.map(option => (
      <ReactNativePicker.Item
        label={option.label}
        value={option.value}
        key={option.value}
      />
    ))}
  </ReactNativePicker>
);

const TimePicker = ({ time, setTime }) => (
  <DateTimePicker
    timeZoneOffsetInMinutes={0}
    value={time}
    mode="datetime"
    is24Hour={true}
    onChange={(_, date) => setTime(date)}
  />
);

export default function Menu(props) {
  const [dataType, setDataType] = useState("str");
  const [averagingWindow, setAveragingWindow] = useState("");
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());

  const [shownElement, setShownElement] = useState("");
  const [isActive, setIsActive] = useState(false);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);

  function showSelector(shownElement) {
    setShownElement(shownElement);
    setIsActive(true);
  }

  function renderSelector(shownElement) {
    switch (shownElement) {
      case "dataType":
        return (
          <Picker
            value={dataType}
            setValue={setDataType}
            options={[
              { label: "Raw", value: "raw" },
              { label: "Strain", value: "str" },
              { label: "Temperature", value: "tmp" }
            ]}
          />
        );
      case "averagingWindow":
        return (
          <Picker
            value={averagingWindow}
            setValue={setAveragingWindow}
            options={[
              { label: "---", value: "" },
              { label: "Millisecond", value: "milliseconds" },
              { label: "Second", value: "second" },
              { label: "Minute", value: "minute" },
              { label: "Hour", value: "hour" },
              { label: "Day", value: "day" },
              { label: "Week", value: "week" },
              { label: "Month", value: "month" }
            ]}
          />
        );
      case "startTime":
        return <TimePicker time={startTime} setTime={setStartTime} />;
      case "endTime":
        return <TimePicker time={endTime} setTime={setEndTime} />;
    }
  }

  return (
    <View
      style={{
        flex: 2,
        borderLeftWidth: 2,
        borderColor: "#404040",
        padding: 10
      }}
      onLayout={event => {
        setWidth(event.nativeEvent.layout.width);
        setHeight(event.nativeEvent.layout.height);
      }}
    >
      <ButtonGroup
        buttons={["Model", "Plot"]}
        selectedIndex={props.mode}
        disabled={props.modelModeEnabled ? [] : [0]}
        onPress={index => props.setMode(index)}
        textStyle={{ fontWeight: "normal" }}
      />
      <Divider />
      <Button
        title="Data Type"
        type={shownElement == "dataType" ? "outline" : "solid"}
        onPress={() => showSelector("dataType")}
      />
      <Divider />
      <Button
        title="Averaging Window"
        type={shownElement == "averagingWindow" ? "outline" : "solid"}
        onPress={() => showSelector("averagingWindow")}
      />
      <Divider />
      <Button
        title="Start Time"
        type={shownElement == "startTime" ? "outline" : "solid"}
        onPress={() => showSelector("startTime")}
      />
      <Divider />
      <Button
        title="End Time"
        type={shownElement == "endTime" ? "outline" : "solid"}
        onPress={() => showSelector("endTime")}
      />
      <Divider />
      <Button
        title="Refresh"
        onPress={() => {
          props.refresh(dataType, averagingWindow, startTime, endTime);
        }}
        type="outline"
        loading={props.isLoading}
        loadingProps={{ size: 16 }}
      />
      <Divider />
      <Modal
        width={width}
        height={height}
        isActive={isActive}
        handleConfirm={() => {
          setIsActive(false);
          setShownElement("");
        }}
      >
        {renderSelector(shownElement)}
      </Modal>
    </View>
  );
}
