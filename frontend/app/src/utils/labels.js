const dataTypeLabels = [
  { label: "Raw", value: "raw" },
  { label: "Strain", value: "str" },
  { label: "Temperature", value: "tmp" },
];

const averagingWindowLabels = [
  { label: "---", value: "" },
  { label: "Millisecond", value: "milliseconds" },
  { label: "Second", value: "second" },
  { label: "Minute", value: "minute" },
  { label: "Hour", value: "hour" },
  { label: "Day", value: "day" },
  { label: "Week", value: "week" },
  { label: "Month", value: "month" },
];

const labels = {
  "Data Type": dataTypeLabels,
  "Averaging Window": averagingWindowLabels,
};

export default labels;
