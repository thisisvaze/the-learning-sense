using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;
using System.Threading.Tasks;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine.UI;

public class JsonData : MonoBehaviour
{

    public static class JsonHelper
    {
        public static T[] FromJson<T>(string json)
        {
            Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
            return wrapper.Items;
        }
        public static string ToJson<T>(T[] array)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper);
        }
        public static string ToJson<T>(T[] array, bool prettyPrint)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper, prettyPrint);
        }
        [Serializable]
        private class Wrapper<T>
        {
            public T[] Items;
        }
    }


    [Serializable]
    public class EnvironmentInfo
    {
        public string name;
        public string x;
        public string y;
        public string z;
    }

    [Serializable]
    public class position
    {
        public string x;
        public string y;
        public string z;
    }
    [Serializable]
    public class info
    {
        public position position;
        public string content;
    }
    [Serializable]
    public class lesson_objects
    {
        public string type;
        public info info;
    }

    [Serializable]
    public class LessonItem
    {
        public lesson_objects[] lesson_objects;
    }


}
