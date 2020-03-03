import React, { useState } from "react";
import { View, Picker } from "react-native";
import { Divider, Button, ButtonGroup } from "react-native-elements";
import DateTimePicker from "@react-native-community/datetimepicker";

export default function Menu(props) {
  const [shownElement, setShownElement] = useState("");
  const [dataType, setDataType] = useState("str");
  const [averagingWindow, setAveragingWindow] = useState("");
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());

  function renderSelector(shownElement) {
    switch (shownElement) {
      case "dt":
        return (
          <>
            <Picker
              selectedValue={dataType}
              onValueChange={(itemValue, itemIndex) => setDataType(itemValue)}
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
            selectedValue={averagingWindow}
            onValueChange={(itemValue, itemIndex) =>
              setAveragingWindow(itemValue)
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
            value={startTime}
            mode="datetime"
            is24Hour={true}
            display="default"
            onChange={(event, date) => setStartTime(date)}
          />
        );
      case "et":
        return (
          <DateTimePicker
            timeZoneOffsetInMinutes={0}
            value={endTime}
            mode="datetime"
            is24Hour={true}
            display="default"
            onChange={(event, date) => setEndTime(date)}
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
        disabled={props.modelModeEnabled ? [] : [0]}
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
          props.refresh(dataType, averagingWindow, startTime, endTime);
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
