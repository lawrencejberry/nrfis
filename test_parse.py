import xml.etree.ElementTree as ET

root = ET.parse("test.moi").getroot()

# print(root.find("ModuleConfiguration").find("IPAddress").text)
# print(root.find("ModuleConfiguration").find("Port").text)


# for sensor in root.iter("SensorConfiguration"):
#     print(
#         sensor.find("Name").text,
#         sensor.find("Reference").text,
#         sensor.find("WavelengthMinimum").text,
#         sensor.find("WavelengthMaximum").text,
#     )

for transducer in root.iter("Transducer"):
    print(transducer.find("ID").text)
    for constant in transducer.iter("TransducerConstant"):
        print("\t", constant.find("Name").text, constant.find("Value").text)
