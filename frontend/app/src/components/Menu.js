import React, { useState } from "react";
import { Platform, View, Picker as WheelPickerIOS } from "react-native";
import { Divider, Button, ButtonGroup, ListItem } from "react-native-elements";
import DateTimePickerIOS from "@react-native-community/datetimepicker";
import { DateTimePickerModal as DateTimePickerAndroid } from "react-native-modal-datetime-picker";

import Modal from "./Modal";

const Picker = ({ value, setValue, options }) => {
  if (Platform.OS === "ios") {
    return (
      <WheelPickerIOS
        selectedValue={value}
        onValueChange={(itemValue, _) => setValue(itemValue)}
      >
        {options.map(option => (
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
      <>
        {options.map((option, _) => (
          <ListItem
            key={option.value}
            title={option.label}
            onPress={() => setValue(option.value)}
            checkmark={option.value === value}
          />
        ))}
      </>
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
        onConfirm={dt => {
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
      ["startTime", "endTime"].includes(shownElement)
    ) {
      setIsDialogActive(true);
    } else {
      setIsModalActive(true);
    }
  }

  function renderButton(element) {
    return (
      <Button
        key={element}
        title={element}
        type={shownElement == element ? "outline" : "solid"}
        onPress={() => showSelector(element)}
      />
    );
  }

  function renderModalSelector(shownElement) {
    switch (shownElement) {
      case "Data Type":
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
      case "Averaging Window":
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
      case "Start Time":
        return (
          <DateTimePicker datetime={startTime} setDatetime={setStartTime} />
        );
      case "End Time":
        return <DateTimePicker datetime={endTime} setDatetime={setEndTime} />;
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
        selectedTextStyle={{ fontWeight: "500" }}
        containerStyle={{ borderColor: "#737f8a", borderWidth: 1 }}
      />
      <Divider />
      {[
        "Data Type",
        "Averaging Window",
        "Start Time",
        "End Time"
      ].map(element => renderButton(element))}
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
        {dialogProps => renderDialogSelector(shownElement, dialogProps)}
      </Dialog>
    </View>
  );
}
