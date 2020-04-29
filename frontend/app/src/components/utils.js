import React from "react";
import { View, Platform } from "react-native";
import { TSpan } from "react-native-svg";

const formatTimestampLabel = (value) => {
  const datetime = new Date(value).toUTCString();
  const date = datetime.slice(5, 16);
  const time = datetime.slice(17, -4);

  const renderLabel = () => (
    <>
      <TSpan>{time}</TSpan>
      <TSpan dx="-4.3em" dy="1.2em">
        {date}
      </TSpan>
    </>
  );

  return Platform.select({
    default: <View style={{ width: 10, height: 10 }}>{renderLabel()}</View>,
    ios: renderLabel(),
  });
};

export default formatTimestampLabel;
