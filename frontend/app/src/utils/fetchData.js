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
    return data;
  } catch (error) {
    console.error(error);
  }
}

// Returns an array of dates between two dates
const getDaysArray = (startTime, endTime) => {
  for (
    const dates = [], d = new Date(startTime);
    d <= endTime;
    d.setDate(d.getDate() + 1)
  ) {
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
      const data = Papa.parse(await response.text()).slice(8);
      temperatureData.push(
        ...data.map((sample) => ({
          timestamp: new Date(date)
            .setHours(...sample[0].split(":"))
            .toISOString(),
          temperature: sample[1],
        }))
      );
    } catch (error) {
      continue;
    }
  }
  return temperatureData;
}
