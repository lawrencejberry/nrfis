import React from "react";

import { Screen } from "../components";
import { BasementModel } from "../models";

export default function BasementScreen() {
  return (
    <Screen packageURL="basement" packageServerName="Basement">
      {(props) => <BasementModel {...props} />}
    </Screen>
  );
}
