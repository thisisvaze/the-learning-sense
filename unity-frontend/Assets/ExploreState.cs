using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine.Windows.Speech;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Collections;
using System.Linq;
using UnityEngine.Windows.WebCam;
using TMPro;
using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.Windows.Speech;
using UnityEngine.UI;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
public class ExploreState : MonoBehaviour
{
    public float delta_x = 0, delta_y = 0, delta_z = 0;
    public GameObject labelType;
    public GameObject[] markers = new GameObject[20];

    // Start is called before the first frame update
    void Start()
    {

        for (int i = 0; i < 20; i++)
        {
            markers[i] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
            markers[i].transform.parent = gameObject.transform;
        }


    }

    void OnEnable()
    {
        //markers[0] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
        EventManager.StartListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);
    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);
    }
    // Update is called once per frame
    void Update()
    {

        gameObject.transform.position = new Vector3(delta_x, delta_y, delta_z);
        //Debug.Log("Object seen: "+envInfo.name);
        // Debug.Log("here: "+ finalPosition);
        //Debug.Log("Text:"+gameObject.transform.position);
        //Debug.Log("Text:"+gameObject.GetComponentInChildren<TMP_Text>().text);
        //gameObject.transform.position = finalPosition;
        //gameObject.transform.rotation =  Camera.main.transform.rotation;
        //gameObject.GetComponentInChildren<TMP_Text>().text = envInfo.name;
    }


    void OnEnvironmentUpdate(string message)
    {

        JsonData.EnvironmentInfo[] EnvInfo = JsonData.JsonHelper.FromJson<JsonData.EnvironmentInfo>(message);
        //Debug.Log("Recieved by Explore State: " + EnvInfo);
        int i = 0;
        if (EnvInfo.Length > 0)
        {

            //Debug.Log(info[0].name);

            //Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
            //Vector3 labdateelFaceRotation = Vector3.Cross(forwardPosition, new Vector3(0,1,0.1)).normalized;
            foreach (JsonData.EnvironmentInfo envInfo in EnvInfo)
            {
                //Debug.Log("Object seen: "+envInfo.name);
                Vector3 finalPosition = new Vector3(0, 0, 0);

                try
                {
                    finalPosition =
                                    new Vector3((float.Parse(envInfo.x)), (float.Parse(envInfo.y)), (float.Parse(envInfo.z)));
                }
                catch
                {
                    // Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
                    // finalPosition = Camera.main.transform.position + 0.8f * forwardPosition +
                    //             new Vector3((float.Parse(envInfo.x)), (float.Parse(envInfo.y)), (float.Parse(envInfo.z)));
                }

                //Camera.main.transform.position + 0.8f*forwardPosition + new Vector3((float.Parse(labelInfo.x)) , (float.Parse(labelInfo.y)) , 0);
                //Debug.Log("here: "+ finalPosition);
                //
                Debug.Log("Object seen: " + envInfo.name);
                Debug.Log("here: " + finalPosition);
                Debug.Log("Text:" + gameObject.transform.position);
                Debug.Log("Text:" + gameObject.GetComponentInChildren<TMP_Text>().text);
                markers[i].transform.localPosition = finalPosition;
                markers[i].transform.rotation = Camera.main.transform.rotation;
                markers[i].GetComponentInChildren<TMP_Text>().text = envInfo.name;

                i++;
            }


        }

    }

}