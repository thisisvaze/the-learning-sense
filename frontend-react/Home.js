import React, { useState, Component, useEffect } from "react";
import * as Constants from "./Constants.js";
import { useFocusEffect } from "@react-navigation/native";
const LinearGradient = require("expo-linear-gradient").LinearGradient;
import {
  Box,
  Stack,
  Heading,
  Text,
  View,
  NativeBaseProvider,
} from "native-base";

const config = {
  dependencies: {
    "linear-gradient": LinearGradient,
  },
};
const Home = () => {
  const [lessons_data, setLessonData] = useState("");
  const [user_pref_data, setUserPrefData] = useState("");
  useFocusEffect(
    React.useCallback(() => {
      fetch(Constants.SERVER_IP + "/get_lessons")
        .then((response) => response.json())
        .then((data) => setLessonData(data))
        .catch((error) => console.error(error));

      // Fetch the second JSON object
      fetch(Constants.SERVER_IP + "/get_user_preferences")
        .then((response) => response.json())
        .then((data) => setUserPrefData(data))
        .catch((error) => console.error(error));

      return () => {
        // Useful for cleanup functions
      };
    }, [])
  );
  return (
    <NativeBaseProvider config={config}>
      <Stack space="4" p="4">
        <Box
          shadow="2"
          rounded="lg"
          w={{ base: "64", md: "80", lg: "md" }}
          _light={{
            bg: {
              linearGradient: {
                colors: ["tertiary.600", "primary.800"],
                start: [0, 0],
                end: [1, 0],
              },
            },
          }}
          _dark={{
            bg: {
              linearGradient: {
                colors: ["tertiary.600", "primary.800"],
                start: [0, 0],
                end: [1, 0],
              },
            },
          }}
        >
          <Stack space="2" p="4">
            <Text color="gray.100">Showing lessons for </Text>
            <Heading color="white">{user_pref_data["topic"]}</Heading>

            <Text pt="3"></Text>
          </Stack>
        </Box>
        <Box
          shadow="2"
          rounded="lg"
          w={{ base: "64", md: "80", lg: "md" }}
          _light={{
            bg: {
              linearGradient: {
                colors: ["tertiary.600", "primary.800"],
                start: [0, 0],
                end: [1, 0],
              },
            },
          }}
          _dark={{
            bg: {
              linearGradient: {
                colors: ["tertiary.600", "primary.800"],
                start: [0, 0],
                end: [1, 0],
              },
            },
          }}
        >
          <Stack space="2" p="4">
            <Text color="gray.100">Total lessons</Text>
            <Heading color="white">{lessons_data.length}</Heading>
          </Stack>
        </Box>
      </Stack>
    </NativeBaseProvider>
  );
};

export default Home;
