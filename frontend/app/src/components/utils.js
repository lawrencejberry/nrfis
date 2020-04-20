import React from "react";
import { TSpan } from "react-native-svg";

const formatTimestampLabel = (value) => {
  const datetime = new Date(value).toUTCString();
  const date = datetime.slice(5, 16);
  const time = datetime.slice(17, -4);
  return (
    <>
      <TSpan>{time}</TSpan>
      <TSpan dx="-4.3em" dy="1.2em">
        {date}
      </TSpan>
    </>
  );
};

export default formatTimestampLabel;
