import React from "react";

import { Screen } from "../components";
import { StrongFloorModel } from "../models";

export default function StrongFloorScreen() {
  return (
    <Screen packageURL="strong-floor" packageServerName="StrongFloor">
      {(props) => <StrongFloorModel {...props} />}
    </Screen>
  );
}
