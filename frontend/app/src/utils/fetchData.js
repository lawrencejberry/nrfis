import Papa from "papaparse";

export default async function fetchData(
  sensorPackage,
  dataType,
  averagingWindow,
  startTime,
  endTime
) {
  try {
    const response = await fetch(
      `http://129.169.72.175/fbg/${sensorPackage}/${dataType}/?averaging-window=${averagingWindow}&start-time=${startTime}&end-time=${endTime}`,
      {
        method: "GET",
        headers: { "media-type": "application/json" },
      }
    );
    const data = await response.json();
    data.forEach((sample) => {
      sample.timestamp = Date.parse(sample.timestamp);
    }); // Store times as Unix timestamps
    return data;
  } catch (error) {
    console.error(error);
  }
}

// Returns an array of dates between two dates
const getDaysArray = (startTime, endTime) => {
  const dates = [];
  for (let d = new Date(startTime); d <= endTime; d.setDate(d.getDate() + 1)) {
    dates.push(new Date(d));
  }
  return dates;
};

export async function fetchTemperatureData(startTime, endTime) {
  const dates = getDaysArray(startTime, endTime);
  const temperatureData = [];
  for (const date of dates) {
    try {
      const response = await fetch(
        `https://www.cl.cam.ac.uk/research/dtg/weather/daily-text.cgi?${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
      );
      const parsedData = Papa.parse(
        (await response.text())
          .split("\n")
          .slice(8, -1)
          .join("\n")
      );
      temperatureData.push(
        ...parsedData.data.map((sample) => ({
          timestamp: date.setHours(...sample[0].split(":")),
          temperature: sample[1],
        }))
      );
    } catch (error) {
      continue;
    }
  }
  return temperatureData;
}
