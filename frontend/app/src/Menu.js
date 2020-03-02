import React, { useState } from "react";
import { View, Picker } from "react-native";
import { Divider, Button, ButtonGroup } from "react-native-elements";
import DateTimePicker from "@react-native-community/datetimepicker";

export default function Menu(props) {
  const [shownElement, setShownElement] = useState("");
  const [modelModeEnabled, setModelModeEnabled] = useState(true);

  function handleDataTypeChange(itemValue, itemIndex) {
    props.setDataType(itemValue);
    if (itemValue == "raw") {
      props.setMode(1);
      setModelModeEnabled(false);
    } else {
      setModelModeEnabled(true);
    }
  }

  function renderSelector(shownElement) {
    switch (shownElement) {
      case "dt":
        return (
          <>
            <Picker
              selectedValue={props.dataType}
              onValueChange={handleDataTypeChange}
            >
              <Picker.Item label="Raw" value="raw" />
              <Picker.Item label="Strain" value="str" />
              <Picker.Item label="Temperature" value="tmp" />
            </Picker>
          </>
        );
      case "aw":
        return (
          <Picker
            selectedValue={props.averagingWindow}
            onValueChange={(itemValue, itemIndex) =>
              props.setAveragingWindow(itemValue)
            }
          >
            <Picker.Item label="---" value="" />
            <Picker.Item label="Millisecond" value="milliseconds" />
            <Picker.Item label="Second" value="second" />
            <Picker.Item label="Minute" value="minute" />
            <Picker.Item label="Hour" value="hour" />
            <Picker.Item label="Day" value="day" />
            <Picker.Item label="Week" value="week" />
            <Picker.Item label="Month" value="month" />
          </Picker>
        );
      case "st":
        return (
          <DateTimePicker
            timeZoneOffsetInMinutes={0}
            value={props.startTime}
            mode="datetime"
            is24Hour={true}
            display="default"
            onChange={(event, date) => props.setStartTime(date)}
          />
        );
      case "et":
        return (
          <DateTimePicker
            timeZoneOffsetInMinutes={0}
            value={props.endTime}
            mode="datetime"
            is24Hour={true}
            display="default"
            onChange={(event, date) => props.setEndTime(date)}
          />
        );
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
    >
      <ButtonGroup
        buttons={["Model", "Plot"]}
        selectedIndex={props.mode}
        disabled={modelModeEnabled ? [] : [0]}
        onPress={index => props.setMode(index)}
        textStyle={{ fontWeight: "normal" }}
      />
      <Divider />
      <Button
        title="Data Type"
        type={shownElement == "dt" ? "outline" : "solid"}
        onPress={() => setShownElement("dt")}
      />
      <Divider />
      <Button
        title="Averaging Window"
        type={shownElement == "aw" ? "outline" : "solid"}
        onPress={() => setShownElement("aw")}
      />
      <Divider />
      <Button
        title="Start Time"
        type={shownElement == "st" ? "outline" : "solid"}
        onPress={() => setShownElement("st")}
      />
      <Divider />
      <Button
        title="End Time"
        type={shownElement == "et" ? "outline" : "solid"}
        onPress={() => setShownElement("et")}
      />
      <Divider />
      <Button
        title="Refresh"
        onPress={() => {
          setShownElement("");
          props.refresh();
        }}
        type="outline"
        loading={props.isLoading}
        loadingProps={{ size: 16 }}
      />
      <Divider />
      {renderSelector(shownElement)}
    </View>
  );
}
