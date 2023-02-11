import { StatusBar } from "expo-status-bar";
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
  const [user_subject, setUserSubject] = useState("");
  const [user_topic, setUserTopic] = useState("");

  const handleUserPrefChangeButton = async () => {
    try {
      const response = await fetch(
        "http://192.168.0.14:8000/update_user_preferences",
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            subject: user_subject,
            topic_of_interest: user_topic,
          }),
        }
      );

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log("data error to server");
      console.error(error);
    }
  };
  return (
    <NativeBaseProvider>
      <ScrollView h="80">
        <Center w="100%">
          <Box safeArea p="2" w="90%" maxW="400" py="8">
            <Heading
              size="lg"
              color="coolGray.800"
              _dark={{
                color: "warmGray.50",
              }}
              fontWeight="semibold"
            >
              Aaditya Vaze
            </Heading>
            <Heading
              mt="1"
              color="coolGray.600"
              _dark={{
                color: "warmGray.200",
              }}
              fontWeight="medium"
              size="xs"
            >
              Topic Preferences
            </Heading>
            <VStack space={3} mt="5">
              <FormControl>
                <FormControl.Label>Subject</FormControl.Label>
                <Input
                  value={user_subject}
                  onChangeText={setUserSubject}
                  placeholder="Enter Subject"
                />
              </FormControl>
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
                Update User Preferences
              </Button>
            </VStack>
          </Box>
        </Center>
      </ScrollView>
    </NativeBaseProvider>
  );
};
export default Profile;
