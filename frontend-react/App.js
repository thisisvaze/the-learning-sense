import React, { useState } from "react";
import {
  View,
  Text,
  Input,
  Button,
  Tag,
  Icon,
  NativeBaseProvider,
} from "native-base";

const TAGS = ["Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5", "Tag 6", "Tag 7"];

const MultiTagInput = () => {
  const [inputValue, setInputValue] = useState("");
  const [tags, setTags] = useState([]);

  const handleInputChange = (value) => {
    setInputValue(value);
  };

  const handleAddTag = () => {
    if (inputValue.trim()) {
      setTags([...tags, inputValue]);
      setInputValue("");
    }
  };

  const handleRemoveTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const renderTag = (tag) => (
    <Tag key={tag}>
      <Text>{tag}</Text>
      <Button transparent onPress={() => handleRemoveTag(tag)}>
        <Icon name="close" />
      </Button>
    </Tag>
  );

  return (
    <NativeBaseProvider>
      <View>
        <Input
          placeholder="Add tags"
          value={inputValue}
          onChangeText={handleInputChange}
        />
        {inputValue ? (
          <View>
            {TAGS.filter((tag) =>
              tag.toLowerCase().includes(inputValue.toLowerCase())
            ).map((tag) => (
              <Button key={tag} onPress={() => setTags([...tags, tag])}>
                <Text>{tag}</Text>
              </Button>
            ))}
          </View>
        ) : null}
        {tags.map(renderTag)}
      </View>
    </NativeBaseProvider>
  );
};

export default MultiTagInput;
