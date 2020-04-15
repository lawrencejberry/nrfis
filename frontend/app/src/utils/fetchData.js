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
        headers: { "media-type": "application/json" }
      }
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}
