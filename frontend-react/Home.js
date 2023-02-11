import React, { Component } from "react";
import {
  Box,
  Stack,
  Heading,
  Text,
  View,
  NativeBaseProvider,
} from "native-base";

class Home extends Component {
  render() {
    return (
      <NativeBaseProvider>
        <Stack space="4" p="4">
          <Box
            shadow="2"
            rounded="lg"
            w={{ base: "64", md: "80", lg: "md" }}
            _light={{ bg: "coolGray.50" }}
            _dark={{ bg: "gray.700" }}
          >
            <Stack space="2" p="4">
              <Text>Showing lessons for </Text>
              <Heading color="emerald.400">Physics, Science</Heading>

              <Text pt="3"></Text>
            </Stack>
          </Box>
          <Box
            shadow="2"
            rounded="lg"
            w={{ base: "64", md: "80", lg: "md" }}
            _light={{ bg: "coolGray.50" }}
            _dark={{ bg: "gray.700" }}
          >
            <Stack space="2" p="4">
              <Text>Total lessons</Text>
              <Heading color="emerald.400">52</Heading>
            </Stack>
          </Box>
        </Stack>
      </NativeBaseProvider>
    );
  }
}

export default Home;
