import React, { useState, Component } from "react";
import {
  Container,
  Content,
  Item,
  Input,
  Icon,
  Label,
  Picker,
  FormControl,
  NativeBaseProvider,
  Text,
} from "native-base";

const options = [
  { label: "Option 1", value: "option1" },
  { label: "Option 2", value: "option2" },
  { label: "Option 3", value: "option3" },
];

const MultiTagInput = () => {
  const [selectedItems, setSelectedItems] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);

  const handleItemPress = (item) => {
    setSelectedItems([...selectedItems, item]);
  };

  const handleRemoveItem = (item) => {
    const updatedItems = selectedItems.filter(
      (selectedItem) => selectedItem !== item
    );
    setSelectedItems(updatedItems);
  };

  return (
    <NativeBaseProvider>
      <Container>
        <FormControl>
          <Icon active name="search" />
          <Input placeholder="Search tags" />
          <Label>Select tag from dropdown:</Label>
          <Picker
            mode="dropdown"
            placeholder="Select tag"
            selectedValue={selectedOption}
            onValueChange={(value) => setSelectedOption(value)}
          >
            {options.map(({ label, value }) => (
              <Picker.Item key={value} label={label} value={value} />
            ))}
          </Picker>
          {selectedItems.map((item) => (
            <Label key={item} style={{ marginRight: 8 }}>
              {item}
              <Icon
                name="close"
                style={{ fontSize: 16, marginLeft: 8 }}
                onPress={() => handleRemoveItem(item)}
              />
            </Label>
          ))}
          <Label>Add tag:</Label>
          <Input
            placeholder="Type tag and press Enter"
            onSubmitEditing={(event) => {
              handleItemPress(event.nativeEvent.text);
              event.target.clear();
            }}
          />
        </FormControl>
      </Container>
    </NativeBaseProvider>
  );
};

class Home extends Component {
  render() {
    return <MultiTagInput></MultiTagInput>;
  }
}
export default Home;
