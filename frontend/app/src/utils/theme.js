const colors = {
  primary: "grey", // "#737f8a"
  secondary: "#404040", // Header bar colour
  actionable: "#2089dc", // Actionable higlight colour
  border: "#d5d5d5",
  background: "white"
};

const theme = {
  colors: colors,
  Text: {
    style: {
      fontSize: 20,
      fontFamily: Platform.select({ default: "Roboto", ios: "Helvetica" })
    }
  },
  Divider: { style: { margin: 4, backgroundColor: colors.border } },
  Button: {
    containerStyle: {
      paddingTop: 5,
      paddingBottom: 5,
      paddingLeft: 10,
      paddingRight: 10
    },
    buttonStyle: { borderWidth: 1 },
    titleStyle: {
      fontSize: 16
    }
  },
  ButtonGroup: { textStyle: { fontSize: 16 } }
};

export default theme;
