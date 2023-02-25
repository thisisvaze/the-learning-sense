import { StatusBar } from "expo-status-bar";
import * as Constants from "./Constants.js";
import {
  ScrollView,
  Input,
  TextArea,
  Button,
  Center,
  Box,
  Heading,
  VStack,
  FormControl,
  NativeBaseProvider,
} from "native-base";
import React, { useState } from "react";

const Profile = () => {
  const [user_topic, setUserTopic] = useState("");

  const handleUserPrefChangeButton = async () => {
    try {
      const response = await fetch(
        Constants.SERVER_IP + "/update_user_preferences",
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            topic: user_topic,
          }),
        }
      );

      const data = await response.json();
      console.log(data);
      alert("User Preferences updated");
    } catch (error) {
      console.log("data error to server");
      console.error(error);
      alert("Error updaing user preferences");
    }
  };
  return (
    <NativeBaseProvider>
      <ScrollView h="80">
        <Center w="100%">
          <Box safeArea p="2" w="90%" maxW="400" py="8">
            <Heading
              size="md"
              color="coolGray.800"
              _dark={{
                color: "warmGray.50",
              }}
              fontWeight="semibold"
            >
              Learning preferences
            </Heading>
            <VStack space={3} mt="5">
              <FormControl>
                <FormControl.Label>Topic</FormControl.Label>
                <Input
                  value={user_topic}
                  onChangeText={setUserTopic}
                  placeholder="Enter topic"
                />
              </FormControl>
              <Button
                onPress={handleUserPrefChangeButton}
                mt="2"
                colorScheme="tertiary"
              >
                Update
              </Button>
            </VStack>
          </Box>
        </Center>
      </ScrollView>
    </NativeBaseProvider>
  );
};
export default Profile;
