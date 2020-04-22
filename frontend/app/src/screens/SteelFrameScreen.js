import React from "react";

import { Screen } from "../components";
import { SteelFrameModel } from "../models";

export default function SteelFrameScreen() {
  return (
    <Screen packageURL="steel-frame" packageServerName="SteelFrame">
      {(props) => <SteelFrameModel {...props} />}
    </Screen>
  );
}
