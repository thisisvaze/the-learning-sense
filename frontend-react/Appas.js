import React, { useState } from "react";
import {
  Container,
  Content,
  Form,
  Item,
  Label,
  Input,
  Button,
  Text,
  NativeBaseProvider,
} from "native-base";

const App = () => {
  const [objectName, setObjectName] = useState("");
  const [subject, setSubject] = useState("");
  const handleSubmit = async () => {
    try {
      const response = await fetch("http://192.168.0.117/add_lesson", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          objectName,
          subject,
        }),
      });
      console.log("data sent to server");
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Object name</Text>
      <Input value={objectName} onChangeText={(text) => setObjectName(text)} />
      <Text>Subject</Text>
      <Input value={subject} onChangeText={(text) => setSubject(text)} />
      <Button onPress={handleSubmit}>
        <Text>Save</Text>
      </Button>
    </View>
  );
};

export default App;
