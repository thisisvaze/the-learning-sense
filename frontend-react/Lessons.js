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
  CheckIcon,
  FormControl,
  Select,
  NativeBaseProvider,
  View,
  Tag,
  StyleSheet,
} from "native-base";
import React, { useState } from "react";
const object_data = [
  "airplane",
  "apple",
  "backpack",
  "banana",
  "baseball bat",
  "baseball glove",
  "bear",
  "bed",
  "bench",
  "bicycle",
  "bird",
  "boat",
  "book",
  "bottle",
  "bowl",
  "broccoli",
  "bus",
  "cake",
  "car",
  "carrot",
  "cat",
  "cell phone",
  "chair",
  "clock",
  "cow",
  "cup",
  "dog",
  "donut",
  "dining table",
  "elephant",
  "fire hydrant",
  "fork",
  "frisbee",
  "giraffe",
  "handbag",
  "hair drier",
  "horse",
  "hot dog",
  "keyboard",
  "kite",
  "knife",
  "laptop",
  "microwave",
  "motorcycle",
  "mouse",
  "orange",
  "oven",
  "parking meter",
  "person",
  "pizza",
  "potted plant",
  "refrigerator",
  "remote",
  "scissors",
  "sheep",
  "sink",
  "skateboard",
  "skis",
  "snowboard",
  "spoon",
  "sports ball",
  "stop sign",
  "suitcase",
  "surfboard",
  "teddy bear",
  "tennis racket",
  "tie",
  "toaster",
  "toilet",
  "toothbrush",
  "traffic light",
  "train",
  "truck",
  "tv",
  "umbrella",
  "vase",
  "wine glass",
  "zebra",
];
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

var objects_list = object_data.map((x) => {
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
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [lessonTitle, setLessonTitle] = useState("");
  const [lessonDescription, setLessonDescription] = useState("");
  const [lessonImageLink, setLessonImageLink] = useState("");
  const [model3D, setModel3D] = useState("");
  const [user_subject, setUserSubject] = useState("");
  const [user_topic, setUserTopic] = useState("");
  const [service, setService] = React.useState("");
  const [tags, setTags] = useState([]);
  const [text, setText] = useState("");
  const addTag = () => {
    if (text.trim() === "") return;

    const newTags = [...tags, text.trim()];
    setTags(newTags);
    setText("");
  };

  const removeTag = (tag) => {
    const newTags = tags.filter((t) => t !== tag);
    setTags(newTags);
  };

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
          tags: [tags],
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
    } catch (error) {
      console.log("data error to server");
      console.error(error);
    }
  };

  return (
    <NativeBaseProvider>
      <ScrollView h="80">
        <Center w="100%">
          <Heading
            size="xl"
            padding={10}
            color="tertiary.500"
            _dark={{
              color: "blue.50",
            }}
            fontWeight="bold"
          >
            XR mini-lesson
          </Heading>
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
              3. Subject
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
                <FormControl.Label>Tags</FormControl.Label>
                <View>
                  <View>
                    {tags.map((tag) => (
                      <Tag key={tag} onPress={() => removeTag(tag)}>
                        <Tag.Label>{tag}</Tag.Label>
                        <Tag.CloseIcon />
                      </Tag>
                    ))}
                  </View>
                  <Input
                    placeholder="Add a tag"
                    value={text}
                    onChangeText={setText}
                    onSubmitEditing={addTag}
                    blurOnSubmit={false}
                  />
                </View>
                {/* {/*  */}
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
