import Papa from "papaparse";

export default async function fetchData(
  sensorPackage,
  dataType,
  averagingWindow,
  startTime,
  endTime
) {
  try {
    // Set up data fetch timeout
    const controller = new AbortController();
    const timeoutID = setTimeout(() => {
      controller.abort();
    }, 15000);
    // Fetch data
    const response = await fetch(
      `http://129.169.72.175/fbg/${sensorPackage}/${dataType}/?averaging-window=${averagingWindow}&start-time=${startTime}&end-time=${endTime}`,
      {
        method: "GET",
        headers: { "media-type": "application/json" },
        signal: controller.signal,
      }
    );
    clearTimeout(timeoutID); // Clear timeout when fetch was successful
    const data = await response.json();
    if (response.status !== 200) {
      throw Error(data.detail);
    }
    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw Error(
        "Too much data to download, please select a smaller time window or larger averaging window"
      );
    } else {
      throw error;
    }
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
          temperature: parseFloat(sample[1]),
        }))
      );
    } catch (error) {
      continue;
    }
  }
  return temperatureData;
}

export async function fetchLiveStatus() {
  const response = await fetch("http://129.169.72.175/fbg/live-status/", {
    method: "GET",
    headers: { "media-type": "application/json" },
  });
  const data = await response.json();
  return data;
}

export async function fetchSensorNames(packageServerName, dataType) {
  const response = await fetch("http://129.169.72.175/openapi.json");
  const data = await response.json();
  const schema = `${packageServerName}_${dataType}`;
  const { timestamp, ...readings } = data.components.schemas[schema].properties;
  const sensorNames = Object.keys(readings);
  return sensorNames;
}
