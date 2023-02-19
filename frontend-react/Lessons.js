import { StatusBar } from "expo-status-bar";
import * as Constants from "./Constants.js";
import { MaterialCommunityIcons } from "@expo/vector-icons";

import {
  ScrollView,
  Input,
  TextArea,
  Button,
  Center,
  Box,
  Heading,
  VStack,
  CheckIcon,
  FormControl,
  Select,
  NativeBaseProvider,
  View,
  Tag,
  StyleSheet,
  Text,
  Icon,
  Ionicons,
  HStack,
} from "native-base";
import React, { useState } from "react";

// const subject_data = [
//   {
//     subject: "Science",
//     topic: ["Physics", "Chemistry", "Biology", "Material Science"],
//   },
//   {
//     subject: "Mathematics",
//     topic: ["Art", "Ideas", "Abstract"],
//   },
//   {
//     subject: "Philosophy",
//     topic: ["Surface Area", "Geometry", "Trigonometry"],
//   },
//   {
//     subject: "History",
//     topic: ["Politics", "Social", "Economic", "Cultural", "intellectual"],
//   },
//   {
//     subject: "Geography",
//     topic: ["Ma", "Geometry", "Trigonometry"],
//   },
//   {
//     subject: "Language",
//     topic: ["French", "German", "Italian"],
//   },
// ];

var objects_list = Constants.object_data.map((x) => {
  return <Select.Item label={x} value={x} />;
});

// var subjects_list = subject_data.map((x) => {
//   return <Select.Item label={x.subject} value={x.subject} />;
// });
// function topics_list(subject) {
//   console.log(subject);
//   if (subject == "") {
//     return "";
//   }
//   return subject_data
//     .filter((x) => x.subject == subject)[0]
//     .topic.map((x) => {
//       return <Select.Item label={x} value={x} />;
//     });
// }

const Lesson = () => {
  const [objectName, setObjectName] = useState("");
  const [lessonTitle, setLessonTitle] = useState("");
  const [lessonDescription, setLessonDescription] = useState("");
  const [lessonImageLink, setLessonImageLink] = useState("");
  const [model3D, setModel3D] = useState("");
  const [inputValue, setInputValue] = useState("");
  const [tags, setTags] = useState([]);

  const handleInputChange = (value) => {
    setInputValue(value);
  };

  const handleAddTag = (tag) => {
    setTags([...tags, tag]);
    setInputValue("");
  };

  const handleRemoveTag = (tag) => {
    setTags(tags.filter((t) => t !== tag));
  };

  const renderTag = (tag) => (
    <Button
      size="sm"
      backgroundColor="tertiary.100"
      variant="subtle"
      onPress={() => handleRemoveTag(tag)}
      endIcon={<Icon as={MaterialCommunityIcons} name="close" size="sm" />}
      marginBottom="0.3em"
    >
      {tag}
    </Button>
  );
  const handleSubmit = async () => {
    try {
      console.log(
        "data" + JSON.stringify({ app: "asdas" }) + " sent to server"
      );
      const response = await fetch(Constants.SERVER_IP + "/add_lessons", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          tags: tags,
          objects: [objectName],
          lesson: {
            template: "TITLE_DESCRIPTION_IMAGE_MODEL",
            lesson_id: "100",
            lesson_curiosity_text: lessonTitle,
            title: lessonTitle,
            description: lessonDescription,
            image_url: lessonImageLink,
            "3d_model": model3D,
          },
        }),
      });

      const data = await response.json();
      console.log(data);
      alert("Lesson added");
    } catch (error) {
      console.log("data error to server");
      console.error(error);
      alert("Error adding lesson");
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
              1. Lesson Anchored object
            </Heading>
            <Heading
              mt="1"
              color="coolGray.600"
              _dark={{
                color: "warmGray.200",
              }}
              fontWeight="medium"
              size="xs"
            ></Heading>
            <VStack space={3} mt="5">
              <FormControl>
                <FormControl.Label>Object</FormControl.Label>
                {/* <Input
                  value={objectName}
                  onChangeText={setObjectName}
                  placeholder="Enter object name Eg. plant, bag, car etc."
                /> */}
                <Select
                  selectedValue={objectName}
                  minWidth="200"
                  accessibilityLabel="Select an object"
                  placeholder="Select an object"
                  _selectedItem={{
                    bg: "teal.600",
                    endIcon: <CheckIcon size="5" />,
                  }}
                  mt={1}
                  onValueChange={setObjectName}
                >
                  {objects_list}
                </Select>
              </FormControl>
            </VStack>
          </Box>
          <Box safeArea p="2" w="90%" maxW="400" py="8">
            <Heading
              size="lg"
              color="coolGray.800"
              _dark={{
                color: "warmGray.50",
              }}
              fontWeight="semibold"
            >
              2. Lesson Content
            </Heading>
            <Heading
              mt="1"
              color="coolGray.600"
              _dark={{
                color: "warmGray.200",
              }}
              fontWeight="medium"
              size="xs"
            ></Heading>
            <VStack space={3} mt="5">
              <FormControl>
                <FormControl.Label>Lesson Title</FormControl.Label>
                <Input
                  value={lessonTitle}
                  onChangeText={setLessonTitle}
                  placeholder="Enter lesson title"
                />
              </FormControl>
              <FormControl>
                <FormControl.Label>Lesson Description</FormControl.Label>
                <TextArea
                  value={lessonDescription}
                  onChangeText={setLessonDescription}
                  placeholder="Enter lesson description"
                />
              </FormControl>
              <FormControl>
                <FormControl.Label>Lesson Image Link</FormControl.Label>
                <Input
                  value={lessonImageLink}
                  onChangeText={setLessonImageLink}
                  placeholder="Enter image link"
                />
              </FormControl>
              <FormControl>
                <FormControl.Label>3D Model</FormControl.Label>
                <Input
                  value={model3D}
                  onChangeText={setModel3D}
                  placeholder="Enter 3D model Eg. plant cell, car engine etc"
                />
              </FormControl>
            </VStack>
          </Box>
          <Box safeArea p="2" w="90%" maxW="400" py="8">
            <Heading
              size="lg"
              color="coolGray.800"
              _dark={{
                color: "warmGray.50",
              }}
              fontWeight="semibold"
            >
              3. Tags
            </Heading>
            <Heading
              mt="1"
              color="coolGray.600"
              _dark={{
                color: "warmGray.200",
              }}
              fontWeight="medium"
              size="xs"
            ></Heading>
            <VStack space={3} mt="5">
              <FormControl>
                <View>
                  <HStack space={2}>{tags.map(renderTag)}</HStack>
                  <Input
                    placeholder="Add tags"
                    value={inputValue}
                    onChangeText={handleInputChange}
                  />
                  {inputValue ? (
                    <View>
                      <Box
                        rounded="lg"
                        overflow="hidden"
                        borderColor="coolGray.200"
                        borderWidth="1"
                        _dark={{
                          borderColor: "coolGray.600",
                          backgroundColor: "gray.700",
                        }}
                        _web={{
                          shadow: 2,
                          borderWidth: 0,
                        }}
                        _light={{
                          backgroundColor: "gray.50",
                        }}
                      >
                        {Constants.TAGS.filter((tag) => !tags.includes(tag))
                          .filter((tag) =>
                            tag.toLowerCase().includes(inputValue.toLowerCase())
                          )
                          .map((tag) => (
                            <Button
                              variant="ghost"
                              key={tag}
                              onPress={() => handleAddTag(tag)}
                            >
                              {tag}
                            </Button>
                          ))}
                      </Box>
                    </View>
                  ) : null}
                </View>
              </FormControl>
              <Button onPress={handleSubmit} mt="2" colorScheme="tertiary">
                Add lesson
              </Button>
            </VStack>
          </Box>
        </Center>
      </ScrollView>
    </NativeBaseProvider>
  );
};

// const styles = StyleSheet.create({
//   container: {
//     flexDirection: "row",
//     alignItems: "center",
//   },
//   tagList: {
//     flexDirection: "row",
//     flexWrap: "wrap",
//     marginRight: 8,
//   },
//   tag: {
//     marginRight: 4,
//   },
// });

export default Lesson;
